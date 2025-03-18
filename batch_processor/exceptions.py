class BatchProcessorError(Exception):
    """Base exception for BatchProcessor."""
    pass


class BatchProcessingRetryError(BatchProcessorError):
    """Raised when a batch exceeds max retry attempts."""
    pass