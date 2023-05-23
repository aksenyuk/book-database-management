import asyncio
import aiohttp
from testing_utils import *

async def stress_test(button, data, num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            task = send_request(session, button, data)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


if __name__ == '__main__':
    button = 'add_button'
    data = {
        'addBookName': 'Book Name3',
        'addBookAuthor': 'Author',
        'addBookYear': '20232',
        'addBookPublisher': 'Publisher'
    }
    num_requests = 100 


    loop = asyncio.get_event_loop()

    results = loop.run_until_complete(stress_test(button, data, num_requests))

    assert results

    for i in results:
        print(i)
    final_data = {'infoBookName': data['addBookName']}
    loop.run_until_complete(check_reservation_status(final_data))
        
    loop.close()
