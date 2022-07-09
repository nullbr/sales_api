## Sales API

Working with FastAPI to practice creating an API with python.

### Dependencies

- python ~> 3.10
- pip ~> 21.3
- postgresql ~> 13

### Installation

Set up virtual environment and install fastapi:

```
$ python3 -m ensurepip
$ python3 -m pip install --user --upgrade pip
$ python3 -m pip install --user virtualenv
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install "fastapi[all]"
```


Setting up the database:

First we need to install PostgreSQL in the machine and create a database for the FastAPI application.
```
$ python3 -m pip install psycopg2-binary  
```