import asyncio
import pytest


from batch_processor import BatchProcessorAsync

class MockSession:
    def close(self):
        pass

@pytest.mark.asyncio
async def test_process_batches_success():
    """
    Testa o processamento bem-sucedido de todos os batches.
    """
    async def mock_query_function(session, batch_size, offset):
        return [{"id": i} for i in range(offset, offset + batch_size)]

    processor = BatchProcessorAsync(
        session_factory=MockSession(),
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

    await asyncio.gather(*successful_batches)
    assert len(successful_batches) == total_rows // batch_size
    assert len(failed_batches) == 0
