import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

import MetaTrader5 as mt5
import onnxruntime as ort
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI

from src.infrastructure.collectors.collector import Collector
from src.infrastructure.Mt5.real_time_mt5 import RealTime
from src.infrastructure.Mt5.historical_mt5 import HistoricalMt5
from src.infrastructure.Buffers.real_data_buffer import RealDataBuffer
from src.infrastructure.Predictor.Predictor import Predictor
from src.application.use_cases.prediction_manager import PredictorManager
from src.infrastructure.adapters.data_collector_adapter import DataCollectorAdapter
from src.application.use_cases.data_ingestion_manager import Collector_Manager
from src.infrastructure.factory.app_factory import AppFactory
from src.infrastructure.config.app_config import AppConfig

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

config = AppConfig(logger)
factory = AppFactory(config, logger)
app_context = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown da aplicação."""
    global app_context
    
    try:
        logger.info("=== Iniciando aplicação ===")
        
        app_context = factory.create_app_context()
        collector_manager = app_context["collector_manager"]
        collector = app_context["collector"]
        
        collector.connect()
        logger.info("Collector conectado")
        
        timeframe = config.get_timeframe()
        task = asyncio.create_task(
            collector_manager.run(timeframe, interval=5.0)
        )
        app_context["task"] = task
        logger.info(f"Coleta iniciada com timeframe={timeframe}")
        yield

    except Exception as e:
        logger.error(f"Erro durante startup: {type(e).__name__}: {e}", exc_info=True)
        raise
    
    finally:
        logger.info("=== Parando aplicação ===")
        
        try:
            if app_context:
                collector_manager = app_context["collector_manager"]
                await collector_manager.stop()
                
                collector = app_context["collector"]
                await collector.stop()

                task = app_context.get("task")
                if task is not None and not task.done():
                    task.cancel()
                
                logger.info("Aplicação parada com sucesso")
        except Exception as e:
            logger.error(f"Erro durante shutdown: {type(e).__name__}: {e}", exc_info=True)


app = FastAPI(
    title="FinKAN",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_context_initialized": app_context is not None
    }


@app.get("/stop")
async def stop_app():
    """Endpoint para parar a aplicação."""
    if app_context:
        app_context["collector_manager"].stop()
        return {"status": "stopped"}
    return {"status": "not_running"}