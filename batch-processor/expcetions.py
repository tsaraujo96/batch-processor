class BatchProcessorError(Exception):
    """Base exception for BatchProcessor."""


class BatchProcessingRetryError(BatchProcessorError):
    """Raised when a batch exceeds max retry attempts."""