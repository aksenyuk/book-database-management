from cassandra.cluster import Cluster
from flask import Flask, request, send_from_directory, jsonify
from utils import *
import threading


# cluster = Cluster(['172.21.0.2'], port=9042)
cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
session = cluster.connect()
session.execute('USE library')

page_name = 'library.html'
app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('', page_name)


def start_server():
     app.run(host='0.0.0.0', port=8089)
    # app.run(port=8080)
    

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    button = data['button']
    if button == 'add_button':
        name = data['addBookName']
        author = data['addBookAuthor']
        year = data['addBookYear']
        publisher = data['addBookPublisher']
        result = add_new_book(session, name, author, year, publisher)
    elif button == 'info_button':
        name = data['infoBookName']
        result = get_book_info(session, name)
    elif button == 'remove_button':
        name = data['removeBookName']
        result = remove_book(session, name)
    elif button == 'reserve_button':
        name = data['reserveBookName']
        card_id = data['reserveCardId']
        result = make_reservation(session, name, card_id)
    elif button == 'return_button':
        name = data['returnBookName']
        result = cancel_reservation(session, name)
    elif button == 'get_list_button':
        books = get_list_of_books(session)
        return jsonify(books=books)
    else:
        result = 'Error'

    return jsonify(result=result)


if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    server_thread.join()