from src.infrastructure.Buffers.real_data_buffer import RealDataBuffer


def test_buffer_starts_empty():
    buffer = RealDataBuffer(batch_size=3)
    assert buffer.size == 0
    assert not buffer.is_full


def test_buffer_is_full_when_batch_size_reached():
    buffer = RealDataBuffer(batch_size=2)
    buffer.add("a")
    assert not buffer.is_full
    buffer.add("b")
    assert buffer.is_full


def test_get_data_returns_copy():
    buffer = RealDataBuffer(batch_size=2)
    buffer.add("a")
    data = buffer.get_data()
    data.append("b")
    assert buffer.size == 1


def test_reset_clears_buffer():
    buffer = RealDataBuffer(batch_size=2)
    buffer.add("a")
    buffer.add("b")
    buffer.reset()
    assert buffer.size == 0
    assert not buffer.is_full
