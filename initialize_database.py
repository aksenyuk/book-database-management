from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
import pandas as pd
import numpy as np


def create_keyspace(
    session,
    keyspace_name, 
    replication_strategy = "SimpleStrategy", 
    replication_factor = 1
):
    create_keyspace_query = f'''CREATE KEYSPACE IF NOT EXISTS {keyspace_name} WITH replication = ''' \
                           f'''{{'class': '{replication_strategy}', 'replication_factor': {replication_factor}}}'''

    session.execute(create_keyspace_query)


def map_pandas_dtype_to_cassandra(pandas_dtype):
    if pandas_dtype == 'int64':
        return 'bigint'
    elif pandas_dtype == 'float64':
        return 'double'
    elif pandas_dtype == 'object':
        return 'text'
    else:
        return 'text'
    

def create_cassandra_table_from_dataframe(session, df, table_name):
    columns = list(df.columns)
    data_types = list(map(map_pandas_dtype_to_cassandra, df.dtypes.tolist()))

    create_table_query = f'''CREATE TABLE IF NOT EXISTS {table_name} (id UUID,'''

    for idx, (column, data_type) in enumerate(zip(columns, data_types)):
        create_table_query += f'''{column} {data_type.upper()}, '''
    
    create_table_query += f'''PRIMARY KEY (book_name));'''
    
    session.execute(create_table_query)
    
    batch_size = 100
    total_rows = len(df)
    num_batches = int(np.ceil(total_rows / batch_size))

    for i in range(num_batches):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, total_rows)
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)

        for _, row in df.iloc[start_index:end_index].iterrows():
            insert_query = f"INSERT INTO {table_name} (id, {', '.join(columns)}) VALUES (uuid(), {', '.join(['%s'] * len(columns))})"
            batch.add(insert_query, row.tolist())

        session.execute(batch)


def main():
    # cluster = Cluster(['172.21.0.2'], port=9042)
    cluster = Cluster(['cassandra1', 'cassandra2', 'cassandra3'])
    session = cluster.connect()

    create_keyspace(session, 'library')
    session.execute('USE library')

    session.execute('DROP TABLE IF EXISTS book_reservations')
    df = pd.read_csv('./dataset.csv')
    print('==> initializing cassandra database ...')
    create_cassandra_table_from_dataframe(session, df, 'book_reservations')
    print('==> database initialized')

    number_of_rows = session.execute('SELECT count(*) FROM book_reservations')
    diff = len(df) - list(next(iter(number_of_rows)))[0]
    if diff != 0:
        print(f'{diff} repetitions in dataset')

    session.shutdown()
    cluster.shutdown()



if __name__ == '__main__':
    main()
