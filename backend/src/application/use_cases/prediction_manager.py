from dataclasses import asdict
import logging

import pandas as pd

from src.domain.interfaces.buffer_interface import BufferInterface
from src.domain.interfaces.batch_registry_interface import BatchRegistryInterface
from src.application.ports.predictor_port import PredictorPort
from src.domain.value_objects.candle_batch import CandleBatch
from src.domain.interfaces.predictor_input_converter import PredictorInputConverter
from src.domain.value_objects.candle_prediction import CandlePrediction
from src.domain.value_objects.candle import Candle
from src.domain.value_objects.raw_data import RawData

logger = logging.getLogger(__name__)


class PredictorManager:
    def __init__(self, predictor : PredictorPort,
                 data_buffer : BufferInterface,
                 candle_buffer : BufferInterface,
                 data_registry: BatchRegistryInterface,
                 pred_registry: BatchRegistryInterface,
                 pred_candle_registry: BatchRegistryInterface,
                 candle_registry: BatchRegistryInterface,
                 converter : PredictorInputConverter
                 ):
        self.data_buffer = data_buffer
        self.candle_buffer = candle_buffer
        self.data_registry = data_registry
        self.pred_registry = pred_registry
        self.pred_candle_registry = pred_candle_registry
        self.candle_registry = candle_registry
        self.predictor = predictor
        self.converter = converter
        self.batch_count = 0

    async def process(self, candle : Candle, data : RawData) -> None:
        try:
            self.data_buffer.add(data)
            self.candle_buffer.add(candle)
            logger.debug(f"Entrada do buffer: {data!r}")

            if not self.data_buffer.is_full:
                return

            input_df = self._flush_buffers()
            prediction = await self.predictor.predict(input_df)
            self._register_prediction(candle.symbol, prediction)
        except Exception as e:
            logger.exception(f"Erro ao processar candle: {type(e).__name__}: {e}")

    def _flush_buffers(self) -> pd.DataFrame:
        """Consolida os buffers em batch, registra e devolve o input do modelo."""
        buffer_data = self.data_buffer.get_data()
        candles = self.candle_buffer.get_data()

        batch_candle = CandleBatch(candles=candles, batch_id=self.batch_count)
        self.batch_count += 1
        self.candle_registry.add(batch_candle)

        input_df = self.converter.convert([asdict(r) for r in buffer_data])
        self.data_registry.add(input_df)

        self.data_buffer.reset()
        self.candle_buffer.reset()
        return input_df

    def _register_prediction(self, symbol: str, prediction) -> None:
        self.pred_registry.add(prediction)
        candle_pred = CandlePrediction(symbol=symbol, raw_data=prediction)
        self.pred_candle_registry.add(candle_pred)
        logger.info(f"Predição registrada para {symbol}: {prediction}")
