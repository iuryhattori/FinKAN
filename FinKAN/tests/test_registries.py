import pytest

from src.infrastructure.storage.batch_candle_registry import BatchCandleRegistry
from src.infrastructure.storage.batch_candle_pred_registry import BatchCandlePredRegistry
from src.infrastructure.storage.batch_matrix_registry import BatchMatrixRegistry
from src.infrastructure.storage.batch_pred_registry import BatchPredRegistry

ALL_REGISTRIES = [
    BatchCandleRegistry,
    BatchCandlePredRegistry,
    BatchMatrixRegistry,
    BatchPredRegistry,
]


@pytest.mark.parametrize("registry_cls", ALL_REGISTRIES)
def test_latest_returns_none_when_empty(registry_cls):
    registry = registry_cls()
    assert registry.latest() is None


@pytest.mark.parametrize("registry_cls", ALL_REGISTRIES)
def test_latest_returns_most_recent(registry_cls):
    registry = registry_cls()
    registry.add("first")
    registry.add("second")
    assert registry.latest() == "second"


@pytest.mark.parametrize("registry_cls", ALL_REGISTRIES)
def test_registry_is_bounded(registry_cls):
    registry = registry_cls(maxlen=3)
    for i in range(10):
        registry.add(i)
    assert len(registry._batches) == 3
    assert registry.latest() == 9


@pytest.mark.parametrize("registry_cls", ALL_REGISTRIES)
def test_reset_clears_and_keeps_maxlen(registry_cls):
    registry = registry_cls(maxlen=2)
    registry.add("a")
    registry.reset()
    assert registry.latest() is None
    for i in range(5):
        registry.add(i)
    assert len(registry._batches) == 2
