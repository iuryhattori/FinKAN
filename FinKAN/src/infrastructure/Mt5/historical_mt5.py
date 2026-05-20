import MetaTrader5 as mt5
from src.domain.interfaces.DataSource_Interface import DataSource_Interface

class HistoricalMt5(DataSource_Interface):
    def __init__(self, login: int, password: str, server: str, start_pos: int = 0):
        self.login = login
        self.password = password
        self.server = server
        self.start_pos = start_pos
        self._positions = {}

    def connect(self) -> None:
        if not mt5.initialize(login=self.login, password=self.password, server=self.server):
            raise ConnectionError(f"MT5 init failed: {mt5.last_error()}")

    def fetch(self, symbol: str, timeframe):
        if not mt5.symbol_select(symbol, True):
            print(f"[MT5] Símbolo '{symbol}' não encontrado no broker")
            return None

        pos = self._positions.get(symbol, self.start_pos)
        raw = mt5.copy_rates_from_pos(symbol, timeframe, pos, 1)

        if raw is None or len(raw) == 0:
            code, msg = mt5.last_error()
            print(f"[MT5 fetch error] symbol='{symbol}' [{code}]: {msg}")
            return None

        self._positions[symbol] = pos + 1
        return raw[0]

    def disconnect(self) -> None:
        mt5.shutdown()