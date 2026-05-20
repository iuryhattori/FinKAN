import traceback
from typing import Any

from dataclasses import asdict
import logging
from src.domain.interfaces.buffer_interface import BufferInterface
from src.application.ports.predictor_port import PredictorPort
from src.domain.interfaces.predictor_input_converter import PredictorInputConverter
from src.domain.entities.Candle import Candle
from src.domain.value_objects.raw_data import RawData
import numpy as np
import asyncio
logger = logging.getLogger(__name__)
class PredictorManager:
    def __init__(self, predictor : PredictorPort,
                 data_buffer : BufferInterface,
                 converter : PredictorInputConverter
                 ):
        self.data_buffer = data_buffer
        self.predictor = predictor
        self.converter = converter

    async def process(self, candle : Candle, data : RawData) -> None:
        try:
            self.data_buffer.add(data)
            logger.info(f"Entrada do buffer: {data!r}")
            if self.data_buffer.is_full:
                logger.debug(f"Conteúdo do buffer: {self.data_buffer.data!r}")
                buffer_data = self.data_buffer.data
                dict_buffer = [asdict(r) for r in buffer_data]
                input = self.converter.convert(dict_buffer)
                
                logger.debug(f"input_df.dtypes:\n{getattr(input, 'dtypes', 'N/A')}")
                logger.debug(f"input_df.head():\n{getattr(input, 'head', lambda: 'N/A')() if hasattr(input, 'head') else 'N/A'}")
                logger.debug(f"input:\n{input}")
                print(input)
                self.data_buffer.reset()

                prediction = await self.predictor.predict(input)
                print(f"Prediction: {prediction}")
        except Exception as e:
            print(f"[ERROR] {type(e).__name__}: {e}")
            traceback.print_exc()