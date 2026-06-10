from pathlib import Path
import os
import logging
import yaml
import MetaTrader5 as mt5


class AppConfig:
    """Carrega e valida configurações da aplicação."""

    def __init__(self, logger : logging.Logger):
        self.config_file = "config.yaml"
        self.logger = logger
        self.config = self._load_config()

    def _load_config(self) -> dict:
        config_file = os.getenv("APP_CONFIG_PATH")
        if config_file:
            config_path = Path(config_file).expanduser().resolve()
        else:
            candidates = [
                Path(__file__).parent / "config.yaml",
                Path(__file__).parents[3] / "config" / "config.yaml",
            ]
            config_path = next((p for p in candidates if p.exists()), candidates[0])
        self.logger.info(f"Carregando configuração de {config_path}")
        if not config_path.exists():
            raise FileNotFoundError(f"Config não encontrado: {config_path}")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def get_symbols(self) -> list[str]:
        """Retorna lista de símbolos do config."""
        return self.config.get("symbols", ["PETR4", "WIN$", "WDO$"])

    def get_model_path(self) -> str:
        """Retorna caminho do modelo ONNX do config."""
        return self.config.get("model_path", "onnx/prediction_1h/prediction_1h.onnx")

    def get_timeframe(self) -> str:
        """Retorna timeframe padrão."""
        return self.config.get("timeframe", mt5.TIMEFRAME_M15)

    def get_buffer_size(self) -> int:
        """Retorna tamanho do buffer."""
        return self.config.get("buffer_size", 4)

    def get_mt5_mode(self) -> str:
        """Retorna o modo de coleta: test ou live."""
        return self.config.get("mt5_mode", os.getenv("MT5_MODE", "live")).lower()

    def get_start_pos(self) -> int:
        """Retorna a posição inicial para testes históricos."""
        return int(self.config.get("start_pos", os.getenv("MT5_START_POS", 0)))

    def get_registry_maxlen(self) -> int:
        """Retorna o tamanho máximo dos registries em memória."""
        return int(self.config.get("registry_maxlen", 256))

    def get_onnx_intra_op_threads(self) -> int | None:
        """Retorna o número de threads da sessão ONNX (None = default do runtime)."""
        value = self.config.get("onnx_intra_op_threads")
        return int(value) if value is not None else None
