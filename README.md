## Sales API

Working with FastAPI to practice creating an API with python.

### Dependencies

- python ~> 3.10
- pip ~> 21.3
- postgresql ~> 13

### Installation

Set up virtual environment and install fastapi:

```
$ python -m ensurepip
$ python -m pip install --user --upgrade pip
$ python -m pip install --user virtualenv
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install "fastapi[all]"
```


Setting up the database:

First we need to install PostgreSQL in the machine and create a database for the FastAPI application.
```
$ python -m pip install psycopg2-binary
$ python -m pip install sqlalchemy
```