import aiohttp
import random
import string

url = 'http://127.0.0.1:8089/process'
headers = {'Content-Type': 'application/json'}


async def send_request(session, button, data):
    payload = {'button': button, **data}
    async with session.post(url, headers=headers, json=payload) as response:
        return await response.json()


async def check_reservation_status(data):
    async with aiohttp.ClientSession() as session:
        button = 'info_button'
        payload = {'button': button, **data}
        async with session.post(url, headers=headers, json=payload) as response:
            result = await response.json()
            print("\n===Final Reservation Status===")
            for i in result['result'].split('<br>'):
                print(i)


async def get_session_book_list():
    async with aiohttp.ClientSession() as session:
        button = 'get_list_button'
        payload = {'button': button}
        async with session.post(url, headers=headers, json=payload) as response:
            result = await response.json()
            return result


def generate_data(button):
    data = {}
    if button == 'add_button':
        data['addBookName'] = generate_random_string()
        data['addBookAuthor'] = generate_random_string()
        data['addBookYear'] = generate_random_year()
        data['addBookPublisher'] = generate_random_string()
    elif button == 'remove_button':
        data['removeBookName'] = generate_random_string()
    elif button == 'info_button':
        data['infoBookName'] = generate_random_string()
    elif button == 'reserve_button':
        data['reserveBookName'] = generate_random_string()
        data['reserveCardId'] = generate_random_card_id()
    elif button == 'return_button':
        data['returnBookName'] = generate_random_string()
    return data


def generate_random_string():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(10))


def generate_random_year():
    return str(random.randint(1900, 2022))


def generate_random_card_id():
    return str(random.randint(1000, 9999))