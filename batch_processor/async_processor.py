import asyncio

class BatchProcessorAsync:
    def __init__(self, session_factory, query_function):
        """
        Initializes the asynchronous batch processor.
        :param session_factory: Function or callable that returns a new database session (Session).
        :param query_function: Function that processes the batch results.
        """
        self.session_factory = session_factory
        self.query_function = query_function

    async def process_batches(self, total_rows, batch_size, num_threads, max_retries=3):
        """
        Processes batches asynchronously, yielding results or failed batches as they complete.
        :param total_rows: Total number of rows in the query.
        :param batch_size: Size of each batch.
        :param num_threads: Number of concurrent tasks.
        :param max_retries: Maximum number of retries for a batch.
        :yield: Tuples of (successful_result, failed_batch).
        """
        queue = asyncio.Queue()

        for offset in range(0, total_rows, batch_size):
            await queue.put(offset)

        async def worker(results):
            """
            Worker function that processes batches and stores the results or errors in a shared list.
            """
            session = self.session_factory
            while not queue.empty():
                offset = await queue.get()
                result = await self.__attempt_batch(session, batch_size, offset, max_retries)
                if result is not None:
                    results.append((result, None))  # Successful result
                else:
                    results.append((None, {"limit": batch_size, "offset": offset}))  # Failed batch
                queue.task_done()

            try:
                session.close()
            except (BaseException,):
                ...


        results = []
        tasks = [worker(results) for _ in range(num_threads)]
        await asyncio.gather(*tasks)

        for result in results:
            yield result

    async def __attempt_batch(self, session, batch_size, offset, max_retries):
        """
        Attempts to process a single batch up to the attempt limit asynchronously.
        :param session: Database session.
        :param batch_size: Size of the batch.
        :param offset: Offset for the query.
        :param max_retries: Maximum retries for processing.
        :return: The result of the batch if successful; otherwise, None.
        """
        attempt = 0
        while attempt < max_retries:
            try:
                result = await self.__run_query_async(session, batch_size, offset)
                return result
            except Exception as e:
                attempt += 1
                print(f"Erro in batch {offset}-{offset + batch_size}, trying {attempt}/{max_retries}: {e}")
        return None

    async def __run_query_async(self, session, batch_size, offset):
        """
        Simulates running the query asynchronously.
        """
        return await asyncio.to_thread(self.query_function, session, batch_size, offset)
