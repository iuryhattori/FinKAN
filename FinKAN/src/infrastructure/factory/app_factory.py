from src.infrastructure.config.app_config import AppConfig
from src.infrastructure.config.predictor_settings import PredictorSettings
from src.infrastructure.Mt5.historical_mt5 import HistoricalMt5
from src.infrastructure.Mt5.real_time_mt5 import RealTime
from src.infrastructure.collectors.collector import Collector
from src.infrastructure.Buffers.real_data_buffer import RealDataBuffer
from src.infrastructure.Predictor.Predictor import Predictor
from src.application.use_cases.prediction_manager import PredictorManager
from src.infrastructure.adapters.data_collector_adapter import DataCollectorAdapter
from src.application.use_cases.data_ingestion_manager import Collector_Manager
from src.infrastructure.conversors.pandas_conversor import PandasPredictorInputConverter
from src.infrastructure.storage.batch_candle_registry import BatchCandleRegistry
from src.infrastructure.storage.batch_matrix_registry import BatchMatrixRegistry
from src.infrastructure.storage.batch_pred_registry import BatchPredRegistry
from src.infrastructure.storage.batch_candle_pred_registry import BatchCandlePredRegistry
import onnxruntime as ort
from typing import Any
import logging
import os


class AppFactory:
    """Factory para criar e gerenciar dependências."""

    def __init__(self, config: AppConfig, logger : logging.Logger):
        self.config = config
        self._session = None
        self.logger = logger
        self._meta_trader = None

    def _create_meta_trader(self) -> Any:
        """Cria conexão MetaTrader5."""
        self.logger.info("Inicializando MetaTrader5...")

        login = int(os.getenv("LOGIN", "0"))
        password = os.getenv("PASSWORD", "")
        server = os.getenv("SERVER", "")
        mode = self.config.get_mt5_mode()

        if mode == "test":
            mt5_instance = HistoricalMt5(
                login=login,
                password=password,
                server=server,
                start_pos=self.config.get_start_pos(),
            )
            self.logger.info("MetaTrader5 inicializado em modo de teste")
        else:
            mt5_instance = RealTime(login=login, password=password, server=server)
            self.logger.info("MetaTrader5 inicializado em modo de produção")

        return mt5_instance

    def _create_onnx_session(self) -> ort.InferenceSession:
        """Carrega modelo ONNX."""
        model_path = self.config.get_model_path()
        self.logger.info(f"Carregando modelo ONNX: {model_path}")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

        session_options = ort.SessionOptions()
        intra_op_threads = self.config.get_onnx_intra_op_threads()
        if intra_op_threads is not None:
            session_options.intra_op_num_threads = intra_op_threads

        session = ort.InferenceSession(
            model_path,
            sess_options=session_options,
            providers=["CPUExecutionProvider"],
        )
        self.logger.info(f"Modelo carregado com sucesso (providers={session.get_providers()})")
        return session

    def create_app_context(self) -> dict:
        """Cria todo o contexto da aplicação."""
        self.logger.info("Criando contexto da aplicação...")

        # Instâncias
        meta_trader = self._create_meta_trader()
        symbols = self.config.get_symbols()

        collector = Collector(symbols, meta_trader)

        session = self._create_onnx_session()

        predictor_settings = PredictorSettings.from_config(self.config.config)

        data_buffer = RealDataBuffer(self.config.get_buffer_size())
        candle_buffer = RealDataBuffer(self.config.get_buffer_size())
        predictor = Predictor(session, predictor_settings)
        conversor = PandasPredictorInputConverter()

        registry_maxlen = self.config.get_registry_maxlen()
        batch_candle_registry = BatchCandleRegistry(maxlen=registry_maxlen)
        batch_matrix_registry = BatchMatrixRegistry(maxlen=registry_maxlen)
        batch_pred_registry = BatchPredRegistry(maxlen=registry_maxlen)
        batch_candle_pred_registry = BatchCandlePredRegistry(maxlen=registry_maxlen)
        prediction_manager = PredictorManager(
            predictor=predictor,
            data_buffer=data_buffer,
            candle_buffer=candle_buffer,
            data_registry=batch_matrix_registry,
            pred_registry=batch_pred_registry,
            candle_registry=batch_candle_registry,
            pred_candle_registry=batch_candle_pred_registry,
            converter=conversor,
        )

        adapter = DataCollectorAdapter(collector)
        collector_manager = Collector_Manager(adapter, prediction_manager)

        self.logger.info("Contexto criado com sucesso")

        return {
            "meta_trader": meta_trader,
            "collector": collector,
            "collector_manager": collector_manager,
            "task": None,
            "predictor": predictor,
            "session": session,
            "batch_candle_pred_registry": batch_candle_pred_registry,
            "batch_candle_registry": batch_candle_registry,
        }
