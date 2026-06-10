import asyncio
import logging
from contextlib import asynccontextmanager
from src.presentation.controllers.predictions import router 
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.presentation.controllers.candle import candle_router
from src.infrastructure.factory.app_factory import AppFactory
from src.infrastructure.config.app_config import AppConfig
from src.presentation.controllers.events import sse_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

config = AppConfig(logger)
factory = AppFactory(config, logger)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown da aplicação."""
    app_context = None
    try:
        logger.info("=== Iniciando aplicação ===")
        
        app_context = factory.create_app_context()
        app.state.app_context = app_context
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Portas do Vite/dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.include_router(candle_router)
app.include_router(sse_router)


@app.get("/health")
async def health_check():
    app_context = getattr(app.state, "app_context", None)
    return {
        "status": "healthy",
        "app_context_initialized": app_context is not None
    }


@app.post("/stop")
async def stop_app():
    app_context = getattr(app.state, "app_context", None)
    if app_context:
        await app_context["collector_manager"].stop()
        return {"status": "stopped"}
    return {"status": "not_running"}