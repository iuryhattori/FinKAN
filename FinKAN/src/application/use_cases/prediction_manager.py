import traceback

from dataclasses import asdict
import logging
from src.domain.interfaces.buffer_interface import BufferInterface
from src.domain.interfaces.batch_interface import batch_interface
from src.application.ports.predictor_port import PredictorPort
from src.domain.value_objects.candle_batch import CandleBatch
from src.domain.interfaces.predictor_input_converter import PredictorInputConverter
from src.domain.value_objects.candle_prediction import CandlePrediction
from src.domain.value_objects.Candle import Candle
from src.domain.value_objects.raw_data import RawData
logger = logging.getLogger(__name__)
class PredictorManager:
    def __init__(self, predictor : PredictorPort,
                 data_buffer : BufferInterface,
                 candle_buffer : BufferInterface,
                 data_registry: batch_interface,
                 pred_registry: batch_interface,
                 pred_candle_registry: batch_interface,
                 candle_registry: batch_interface,
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
            logger.info(f"Entrada do buffer: {data!r}")
            if self.data_buffer.is_full:
                logger.debug(f"Conteúdo do buffer: {self.data_buffer.data!r}")
                buffer_data = self.data_buffer.get_data()
                candles = self.candle_buffer.get_data()
                batch_candle = CandleBatch(candles = candles, batch_id = self.batch_count)
                self.batch_count += 1
                self.candle_registry.add(batch_candle)
                dict_buffer = [asdict(r) for r in buffer_data]
                input = self.converter.convert(dict_buffer)
                # matrix = self.converter.convert_to_matrix(input)
                self.data_registry.add(input)
                logger.debug(f"input_df.dtypes:\n{getattr(input, 'dtypes', 'N/A')}")
                logger.debug(f"input_df.head():\n{getattr(input, 'head', lambda: 'N/A')() if hasattr(input, 'head') else 'N/A'}")
                logger.debug(f"input:\n{input}")
                print(input)
                self.data_buffer.reset()
                self.candle_buffer.reset()
                prediction = await self.predictor.predict(input)
                self.pred_registry.add(prediction)
                candle_pred = CandlePrediction(symbol=candle.symbol, raw_data=prediction)
                self.pred_candle_registry.add(candle_pred)
                print(f"Prediction: {prediction}")
        except Exception as e:
            print(f"[ERROR] {type(e).__name__}: {e}")   
            traceback.print_exc()