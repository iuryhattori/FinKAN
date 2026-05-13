import asyncio
from concurrent.futures import thread
from multiprocessing import process
from platform import processor
import MetaTrader5 as mt5
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.pipeline.collector import collector
from src.pipeline.meta_trader.Mt5 import Mt5
from src.pipeline.collector.collector import Collector
from src.pipeline.preprocessing.preprocess import FrameProcessor
from threading import Thread
from dotenv import load_dotenv
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app : FastAPI):
    login_env = os.getenv("LOGIN")
    login_int = int(login_env)
    password = os.getenv("PASSWORD")
    server = os.getenv("SERVER")
    meta_trader = Mt5(login=login_int, password=password, server=server)
    names = ["PETR4", "WIN$", "WDO$"]
    processor = FrameProcessor(names)
    collector = Collector(names, meta_trader, processor)

    collector.connect()
    thread = Thread(target=collector.collect, args= (mt5.TIMEFRAME_M15,), daemon=True)
    thread.start()

    yield

    collector.stop()
    thread.join(timeout=5)
app = FastAPI(lifespan=lifespan)

    