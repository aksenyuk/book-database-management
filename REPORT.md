# Library Book and their Reservation Management

---
**Team members:**

- Sofya Aksenyuk, 150284
- Uladzimir Ivashka, 150281

---

The System makes it possible to make, update/cancel, see book reservation, as well as add/remove a book to/from the library.

All the operations are handled through a webpage.

## How to run it

- Build image: `docker build -t my_flask_server:latest .`
- Start app: `docker compose up`
    - Access webpage via search tab: `localhost:80`
- Run stress tests: `bash run_tests.sh`

## Description

There's a multi-container setup, five services total:

 - three Cassandra database nodes
 - Flask web server app
 - Nginx web server used as a reverse proxy
 
The services are connected using a bridge network named cassandra-net.

Taking a look at docker-compose.yml:

- `cassandra1`, `cassandra2`, `cassandra3` are based on the cassandra:latest image
    - All the Cassandra containers expose port 9042
    - The healthcheck parameter runs a CQLSH command to describe the keyspaces in the database, testing the health of each instance. It is repeated every 5 seconds with a maximum of 60 retries
    - The `cassandra2` and `cassandra3` instances have dependencies on the health of the previous instances (`cassandra1` and `assandra2`, respectively), ensuring that the next instance won't start before the previous one is healthy

 - `flask_server` is a Flask web app service built from a custom image my_flask_server
    - This service has a memory limit of 1GB and it's dependent on the `cassandra3` service being healthy before starting
    - The ports 8089 to 8091 are exposed and mapped to the same ports in the container
    - Under the deploy parameter, three replicas of the Flask service are to be created, providing load balancing across multiple instances of the service
    - The server firstly initializes the database (running `initialize_database.py` script), later posting `library.html` as a webpage

- `nginx` is based on the nginx:latest image
    - Nginx is configured to listen on port 80 and is dependent on the flask_server service
    - The volume mapping `./nginx.conf:/etc/nginx/conf.d/default.conf` is used as the default configuration file within the Nginx container

Taking a look at `./tests` directory:

There are five stress tests defined (`testing_utils.py` comprises of common functions used for them).

Main takeaways of each stress test:

- Simulates a real-world situation, e.g.:
    - entering the same book data as an input for the same action
    - creating/deleting the same book
    - reserving/unreserving the same book
    - ...
- Is being run asyncronously 
- Communicates with the database through `library.html`, getting/posting user input data from/to the webpage

Database schema:

library.book_reservations (
    book_name text PRIMARY KEY,
    book_author text,
    id uuid,
    is_reserved bigint,
    publisher text,
    reserver_card_id bigint,
    year text
) 

where,

- library is KEYSPACE
- book_reservations is TABLE

See dataset: [Dataset](https://raw.githubusercontent.com/Giminosk/book-database-management/main/data/dataset.csv)

## Problems encountered

- When not using `healthcheck`, the database was getting initialized before the nodes were fully up
- When not defining `MAX_HEAP_SIZE` and `HEAP_NEWSIZE`, RAM usage used to explode
- Improper `nginx` configuration lead to various problems with ports
- Communication between nodes is still not fast enough to proceed several requests paralelly (e.g., book gets inserted several times, since the previous information about it was not yet delivered). Note: Happens due to the extreme speed of async requests. When using `requests` library, the problem was not met.
