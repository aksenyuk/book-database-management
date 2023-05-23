import asyncio
import aiohttp
from testing_utils import *


async def stress_test(client_id, book_name, num_requests):
    async with aiohttp.ClientSession() as session:
        reserve_data = {
            'reserveBookName': book_name,
            'reserveCardId': client_id
        }
        return_data = {
            'returnBookName': book_name
        }

        reserve_tasks = list()
        return_tasks = list()
        for _ in range(num_requests):
            reserve_task = send_request(session, 'reserve_button', reserve_data)
            return_task = send_request(session, 'return_button', return_data)
            reserve_tasks.append(reserve_task)
            return_tasks.append(return_task)

        results = await asyncio.gather(*reserve_tasks, *return_tasks)
        return results

if __name__ == '__main__':
    book_name = 'Lolita' 
    client_id = '11'
    num_requests = 1000

    loop = asyncio.get_event_loop()
    task = stress_test(client_id, book_name, num_requests)

    results = loop.run_until_complete(asyncio.gather(task))

    assert results

    for result in results:
        print(result) 
    loop.close()
