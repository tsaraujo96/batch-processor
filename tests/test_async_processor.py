import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from batch_processor import BatchProcessorAsync

@pytest.mark.asyncio
async def test_process_batches_success():
    """
    Testa o processamento bem-sucedido de todos os batches.
    """
    async def mock_query_function(session, batch_size, offset):
        return [{"id": i} for i in range(offset, offset + batch_size)]

    def mock_session_factory():
        return "MockSession"

    processor = BatchProcessorAsync(
        session_factory=mock_session_factory,
        query_function=mock_query_function,
    )

    total_rows = 1000
    batch_size = 100
    num_threads = 5

    successful_batches = []
    failed_batches = []

    async for success, failure in processor.process_batches(
        total_rows=total_rows,
        batch_size=batch_size,
        num_threads=num_threads
    ):
        if success:
            successful_batches.append(success)
        if failure:
            failed_batches.append(failure)

    assert len(successful_batches) == total_rows // batch_size
    assert len(failed_batches) == 0


@pytest.mark.asyncio
async def test_process_batches_with_failures():
    """
    Testa o processamento de batches com falhas simuladas.
    """
    async def mock_query_function(session, batch_size, offset):
        if offset == 300:
            raise Exception(f"Simulated failure at offset {offset}")
        return [{"id": i} for i in range(offset, offset + batch_size)]

    def mock_session_factory():
        return "MockSession"

    processor = BatchProcessorAsync(
        session_factory=mock_session_factory,
        query_function=mock_query_function,
    )

    total_rows = 1000
    batch_size = 100
    num_threads = 5

    successful_batches = []
    failed_batches = []

    async for success, failure in processor.process_batches(
        total_rows=total_rows,
        batch_size=batch_size,
        num_threads=num_threads
    ):
        if success:
            successful_batches.append(success)
        if failure:
            failed_batches.append(failure)

    assert len(successful_batches) == (total_rows // batch_size) - 1
    assert len(failed_batches) == 1
    assert failed_batches[0]["offset"] == 300
