import asyncio
import aiohttp
from testing_utils import *


async def reserve_books(user_id, book_list):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for book in book_list:
            button = 'reserve_button'
            data = {'reserveBookName': book, 'reserveCardId': user_id}
            task = send_request(session, button, data)
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        print(results)
        return results


if __name__ == '__main__':
    user1_id = '1'
    user2_id = '2'
    
    loop = asyncio.get_event_loop()

    book_list = loop.run_until_complete(get_session_book_list())
    book_list = book_list['books'].split('<br>•')
    # 1000, because we dont have so much ram (and time)
    book_list = list(map(lambda x: x.replace('•', '').replace('<br>', '').strip(), book_list))

    tasks = [reserve_books(user1_id, book_list), reserve_books(user2_id, book_list)]
    results = loop.run_until_complete(asyncio.gather(*tasks))

    assert results

    for user_results in results:
        for result in user_results:
            print(result)  
    
    loop.close()
