import asyncio
import aiohttp
import random
from testing_utils import *


async def stress_test(client_id):
    async with aiohttp.ClientSession() as session:
        actions = ['add_button', 'remove_button', 'info_button', 'reserve_button', 'return_button']
        num_requests = 100
        tasks = []
        for _ in range(num_requests):
            button = random.choice(actions)
            data = generate_data(button)
            task = send_request(session, button, data)
            tasks.append(task)
            print(client_id, button)
        results = await asyncio.gather(*tasks)
        return results


if __name__ == '__main__':
    clients = ['Client1', 'Client2', 'Client3']

    loop = asyncio.get_event_loop()
    tasks = []
    for client_id in clients:
        task = stress_test(client_id)
        tasks.append(task)
    results = loop.run_until_complete(asyncio.gather(*tasks))

    assert results
    
    loop.close()
