import asyncio
from concurrent.futures import thread
from multiprocessing import process
from platform import processor
import MetaTrader5 as mt5
from contextlib import asynccontextmanager
from fastapi import FastAPI
from FinKAN.src.pipeline.collector import collector
from src.pipeline.meta_trader.Mt5 import Mt5
from src.pipeline.collector.collector import Collector
from src.pipeline.preprocessing.preprocess import FrameProcessor
from threading import Thread


@asynccontextmanager
async def lifespan(app : FastAPI):
    meta_trader = Mt5()
    names = ["PETR4", "WIN$", "WDO$"]
    processor = FrameProcessor(names)
    collector = Collector(names, meta_trader, processor)

    collector.connect()
    thread = Thread(targe=collector.collect, args= (mt5.TIMEFRAME_M1,), daemon=True)
    thread.start()

    yield

    collector.stop()
    thread.join(timeout=5)
app = FastAPI(lifespan=lifespan)

    