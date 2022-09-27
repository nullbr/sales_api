## Sales API

Working with FastAPI to practice creating an API with python.

### Dependencies

- python ~> 3.10
- pip ~> 21.3
- postgresql ~> 13

### Installation

Set up virtual environment and install fastapi:

```
$ sudo apt install python3-pip
$ python3 -m pip install --user --upgrade pip
$ python3 -m pip install --user virtualenv
$ sudo apt-get install python3-venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install "fastapi[all]"
```


Setting up the database:

First we need to install PostgreSQL in the machine and create a database for the FastAPI application.
```
$ pip install psycopg2-binary
$ pip install sqlalchemy
```

Password Encryption:
```
$ pip install passlib[bycrypt]
```

Auth token generation:
```
$ pip install "python-jose[cryptography]"
```

Run the app from root directory:

```
$ uvicorn app.main:app --reload
```

### Load API
```
source venv/bin/activate
uvicorn app.main:app --reload
```