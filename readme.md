# Batch Processor

**Batch Processor** is a Python library for processing data in batches using asynchronous programming. This library is designed to handle large datasets efficiently by dividing them into manageable chunks, processing each batch concurrently, and retrieving results incrementally. It is particularly useful for applications that interact with databases or large APIs.

---

## Features
- **Asynchronous Processing**: Utilize `asyncio` for high-performance, non-blocking execution.
- **Batch Management**: Break down large datasets into smaller, easier-to-handle chunks.
- **Failure Recovery**: Track and report failed batches for retries or debugging.
- **Customizable**: Easily integrate your own session factory and query logic.

---

## Installation
Install the library using `pip`:

```bash
pip install batch-processor
```

## Usage
Here's a step-by-step guide to using the Batch Processor in your application.

### Step 1: Define a Query Function
The query function retrieves data for a specific batch. It must accept the following parameters.

- **`session`**: The database session.
- **`batch_size`**: The size of the batch.
- **`offset`**: The offset to start the batch.

Example:
```python
async def query_function(session, batch_size, offset):
    # Mocked query for illustration
    return [{"id": i} for i in range(offset, offset + batch_size)]
```
### Step 2: Define a Session Factory
The session factory should return a database session or any equivalent connection. For testing, you can use a mock session.

Example:
```python
def session_factory():
    # Mocked database session for demonstration
    return "MockSession"
```
### Step 3: Instantiate and Run BatchProcessorAsync
Use the `BatchProcessorAsync` to process your data in batches:

```python
import asyncio
from batch_processor import BatchProcessorAsync

async def main():
    processor = BatchProcessorAsync(
        session_factory=session_factory,
        query_function=query_function,
    )

    total_rows = 1000  # Total number of rows in the dataset
    batch_size = 100   # Number of rows per batch
    num_threads = 5    # Number of concurrent workers

    async for success, failure in processor.process_batches(
        total_rows=total_rows,
        batch_size=batch_size,
        num_threads=num_threads,
    ):
        if success:
            print("Processed successfully:", success)
            # make your operations
        if failure:
            print("Failed batch:", failure)
            # make your operations

# Run the asynchronous main function
asyncio.run(main())
```
### Step 4: Handle Failed Batches
You can collect and retry failed batches if needed

Example:
```python
async def main():
    processor = BatchProcessorAsync(
        session_factory=session_factory,
        query_function=query_function,
    )

    failed_batches = []
    async for success, failure in processor.process_batches(
        total_rows=1000,
        batch_size=100,
        num_threads=5,
    ):
        if failure:
            failed_batches.append(failure)

    print("Failed Batches:", failed_batches)
```

## Advanced Usage
### Custom Retry Logic
You can customize the retry logic for handling failed batches by setting `max_retries`:

```python
async for success, failure in processor.process_batches(
    total_rows=1000,
    batch_size=100,
    num_threads=5,
    max_retries=5,  # Increases retry attempts
):
    ...
```
### Using Real Databases
For real-world use, replace the mock functions with actual database connections and queries, you can use raw statement or ORM statement:

- ORM example:
```python
async def real_query_function(session, batch_size, offset):
    # Replace with your database query logic
    return session.query(Model).limit(batch_size).offset(offset).all()
```

- Raw example:
```python
async def real_query_function(session, limit: int, offset: int):
    try:
         # Replace with your database query logic
        raw_query = text("SELECT * FROM table_name LIMIT :limit OFFSET :offset")
        result = session.execute(raw_query, {"limit": limit, "offset": offset})

        results = result.fetchall()
        return results
    except SQLAlchemyError as e:
        raise e
```
