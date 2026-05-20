from typing import Tuple
import inspect
from src.domain.interfaces.collector_interface import Collector_Interface
from src.application.ports.data_collector_port import DataCollectorPort
import asyncio
from src.application.helpers.helper import raw_to_wide_record
from src.domain.value_objects.raw_data import RawData
from src.domain.entities.Candle import Candle

class DataCollectorAdapter(DataCollectorPort):
    def __init__(self, collector: Collector_Interface, target_symbol: str = "PETR4"):
        self.collector = collector
        self.target_symbol = target_symbol
    
    async def connect(self):
        if inspect.iscoroutinefunction(self.collector.connect):
            return await self.collector.connect()
        else:
            return await asyncio.to_thread(self.collector.connect)
    
    async def stop(self):
        if inspect.iscoroutinefunction(self.collector.stop):
            return await self.collector.stop()
        else:
            return await asyncio.to_thread(self.collector.stop)

    async def collect_data(self, timeframe : str) -> Tuple[Candle, RawData]:
        if inspect.iscoroutinefunction(self.collector.collect):
            candles = await self.collector.collect(timeframe)
        else:
            candles = await asyncio.to_thread(self.collector.collect, timeframe)
        petr4 = candles["PETR4"]
        wdo = candles["WDO$"]
        win = candles["WIN$"]

        if self.target_symbol not in candles:
            raise ValueError(f"{self.target_symbol} not found in collected candles: {list(candles.keys())}")
        data = candles[self.target_symbol]
        candle = Candle(
            open=data[1],
            high=data[2],
            low=data[3],
            close=data[4],
            tick_vol=data[5],
            date=data[0],
            symbol=self.target_symbol
        )
        record = raw_to_wide_record(petr4, wdo, win)
        return candle, record