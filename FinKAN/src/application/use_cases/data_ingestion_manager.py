from src.domain.interfaces.collector_interface import Collector_Interface
from src.application.ports.data_collector_port import DataCollectorPort
import asyncio
import traceback
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Collector_Manager:
    def __init__(
        self, 
        collector_adapter: DataCollectorPort,
        prediction_manager,
        max_retries: int = 3,
        backoff_factor: float = 2.0
    ):
        self.collector_adapter = collector_adapter
        self.prediction_manager = prediction_manager
        self._active = True
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
        self._task: asyncio.Task = None

    async def run(self, timeframe: str, interval: float = 5.0) -> None:
        """
        Executa coleta de dados continuamente com retry e rate limiting.
        
        Args:
            timeframe: Período de tempo (ex: "M15")
            interval: Intervalo entre tentativas (segundos)
        """
        self._active = True
        retry_count = 0
        
        logger.info(f"Iniciando coleta: timeframe={timeframe}, interval={interval}s")
        await self.collector_adapter.connect()
        try:
            while self._active:
                try:
                    candle, data = await self.collector_adapter.collect_data(timeframe)
                    
                    await self.prediction_manager.process(candle, data)
                    retry_count = 0
                    await asyncio.sleep(interval)
                
                except asyncio.CancelledError:
                    logger.info("Coleta cancelada")
                    break
                    
                except ConnectionError as e:
                    retry_count += 1
                    if retry_count > self._max_retries:
                        logger.error(f"Max retries atingido para ConnectionError: {e}")
                        break
                        
                    wait_time = interval * (self._backoff_factor ** (retry_count - 1))
                    logger.warning(
                        f"Erro de conexão. Retry {retry_count}/{self._max_retries} "
                        f"em {wait_time:.1f}s: {e}"
                    )
                    await asyncio.sleep(wait_time)
                    
                except Exception as e:
                    logger.error(
                        f"Erro inesperado: {type(e).__name__}: {e}",
                        exc_info=True
                    )
                    await asyncio.sleep(interval)
        finally:
            await self.collector_adapter.stop()

    async def stop(self) -> None:
        logger.info("Parando coleta de dados...")
        self._active = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                logger.info("Task de coleta cancelada")
            self._task = None

    async def start(self, timeframe: str, interval: float = 5.0) -> None:
        if self._task and not self._task.done():
            logger.warning("Coleta já está ativa. Ignorando novo start.")
            return
        self._task = asyncio.create_task(self.run(timeframe, interval))