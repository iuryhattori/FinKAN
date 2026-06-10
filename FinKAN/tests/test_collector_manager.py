from src.application.use_cases.data_ingestion_manager import Collector_Manager


class FakeAdapter:
    def __init__(self, error: Exception = None):
        self.error = error
        self.connect_calls = 0
        self.stop_calls = 0
        self.collect_calls = 0

    async def connect(self):
        self.connect_calls += 1

    async def stop(self):
        self.stop_calls += 1

    async def collect_data(self, timeframe):
        self.collect_calls += 1
        if self.error is not None:
            raise self.error
        return "candle", "data"


class FakePredictionManager:
    def __init__(self, manager_holder):
        self.calls = []
        self.manager_holder = manager_holder

    async def process(self, candle, data):
        self.calls.append((candle, data))
        # Encerra o loop após a primeira coleta bem-sucedida.
        self.manager_holder["manager"]._active = False


async def test_run_collects_and_forwards_to_prediction_manager():
    adapter = FakeAdapter()
    holder = {}
    prediction_manager = FakePredictionManager(holder)
    manager = Collector_Manager(adapter, prediction_manager)
    holder["manager"] = manager

    await manager.run("M15", interval=0)

    assert adapter.connect_calls == 1
    assert prediction_manager.calls == [("candle", "data")]
    assert adapter.stop_calls == 1


async def test_run_stops_after_max_retries_on_connection_error():
    adapter = FakeAdapter(error=ConnectionError("MT5 down"))
    manager = Collector_Manager(
        adapter,
        prediction_manager=None,
        max_retries=2,
        backoff_factor=1.0,
    )

    await manager.run("M15", interval=0)

    # 2 retries + a tentativa que excede o limite
    assert adapter.collect_calls == 3
    assert adapter.stop_calls == 1


async def test_start_ignores_duplicate_start():
    adapter = FakeAdapter(error=ConnectionError("MT5 down"))
    manager = Collector_Manager(adapter, prediction_manager=None, max_retries=1)

    await manager.start("M15", interval=0)
    first_task = manager._task
    await manager.start("M15", interval=0)
    assert manager._task is first_task

    await manager.stop()
    assert manager._task is None
