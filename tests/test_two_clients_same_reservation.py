import asyncio
import aiohttp
from testing_utils import *


async def stress_test(button, data, num_requests, reserve_card_id):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            data['reserveCardId'] = f'{reserve_card_id}'
            task = send_request(session, button, data)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        for result in results:
            print(reserve_card_id, result)      
        return True
    

if __name__ == '__main__':
    button = 'reserve_button'
    data = {
        'reserveBookName': 'test_book',
    }
    num_requests = 200
    client1_id = '1'
    client2_id = '2'

    loop = asyncio.get_event_loop()
    
    clients_results = loop.run_until_complete(asyncio.gather(
        stress_test(button, data, num_requests, client1_id),
        stress_test(button, data, num_requests, client2_id)
    ))

    assert clients_results

    final_data = {'infoBookName': data['reserveBookName']}
    result = loop.run_until_complete(check_reservation_status(final_data))

    loop.close()
