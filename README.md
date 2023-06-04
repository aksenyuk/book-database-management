# Library Book and their Reservation Management 

The System makes it possible to make, update/cancel, see book reservation, as well as add/remove a book to/from the library.

All the operations are handled through a webpage.

Read Full Description: [Description](https://github.com/Giminosk/book-database-management/blob/main/REPORT.md)

## How to run it

- Build image: `docker build -t my_flask_server:latest .`
- Start app: `docker compose up`
    - Access webpage via search tab: `localhost:80`
- Run stress tests: `bash run_tests.sh`
