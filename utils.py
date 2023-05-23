def add_new_book(session, name, author, year, publisher):

    book_name = name.strip().replace("'", "''")
    select_query = '''SELECT is_reserved FROM book_reservations WHERE book_name = %s;'''
    result = session.execute(select_query, [book_name])
    if result:
        return "Book already exist"

    column_names = list(session.execute('''SELECT * FROM book_reservations LIMIT 1''').column_names)
    column_names.remove('id')

    user_input = {
        'book_name': name, 
        'book_author': author, 
        'year': year, 
        'publisher': publisher, 
        'is_reserved': 0, 
        'reserver_card_id': -1
    }

    insert_query = f'''INSERT INTO book_reservations (id, {', '.join(list(user_input.keys()))}) ''' \
                   f'''VALUES (uuid(), {', '.join(['%s'] * len(user_input))})'''
    values = list(user_input.values())
    session.execute(insert_query, values)
    return f'Book inserted<br><br>{get_book_info(session, name)}'



def remove_book(session, book_name):
    book_name = book_name.strip().replace("'", "''")
    delete_query = '''DELETE FROM book_reservations WHERE book_name = %s IF EXISTS;'''
    result = session.execute(delete_query, [book_name])
    if result.one().applied:
        return "Book deleted"
    else:
        return "Book does not exist"



def get_book_info(session, book_name):
    book_name = book_name.strip().replace("'", "''")
    select_query = '''SELECT * FROM book_reservations WHERE book_name = %s;'''
    result = session.execute(select_query, [book_name])
    if result:
        out = ""
        row = next(iter(result))
        for column_name in row._fields:
            if column_name not in ('id'):
                column_value = getattr(row, column_name)
                if column_name == 'is_reserved':
                    column_value = ('No', 'Yes')[column_value]
                if column_name == 'reserver_card_id' and int(column_value) == -1:
                    continue
                out += "{: >25} {: >25}<br>".format(column_name, column_value)
        return out
    else:
        return "Book does not exist"



def make_reservation(session, book_name, user_id):
    book_name = book_name.strip().replace("'", "''")
    select_query = '''SELECT is_reserved FROM book_reservations WHERE book_name = %s;'''
    result = session.execute(select_query, [book_name])

    if not result:
        return "Book does not exist"
    result = list(next(iter(result)))[0]
    if result == 1:
        return "Book is already reserved"

    update_query = "UPDATE book_reservations SET is_reserved = %s, reserver_card_id = %s WHERE book_name = %s"
    session.execute(update_query, [1, int(user_id), str(book_name)])
    return f'You have reserved book <br><br>{get_book_info(session, book_name)}'



def cancel_reservation(session, book_name):
    book_name = book_name.strip().replace("'", "''")
    select_query = '''SELECT is_reserved FROM book_reservations WHERE book_name = %s;'''
    result = session.execute(select_query, [book_name])

    if not result:
        return "Book does not exist"
    result = list(next(iter(result)))[0]
    if result == 0:
        return "You cannot return the book, because it is not reserved"

    update_query = "UPDATE book_reservations SET is_reserved = %s, reserver_card_id = %s WHERE book_name = %s"
    session.execute(update_query, [0, -1, str(book_name)])
    return f'You have returned book <br><br>{get_book_info(session, book_name)}'


def get_list_of_books(session):
    select_query = '''SELECT book_name FROM book_reservations limit 1000;'''
    result = session.execute(select_query)
    result = list(result)
    return_string = ""
    for book in result:
        return_string += f'• {str(book.book_name)} <br>'
    return return_string