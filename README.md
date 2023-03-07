## Sales API
https://bruno.buzz/docs

Working with FastAPI to practice creating an API with python.
Deployed to ubuntu server in DigitalOcean.
Fully Dockerized application.
Using TestClient for automated testing.

### Dependencies

- python ~> 3.10
- pip ~> 21.3
- postgresql ~> 13

### Production set up
Production machine is ubuntu 18.04 on DigitalOcean
domain used is bruno.buzz
gunicorn to handle process managment
nginx for ssl
certbot for HTTPS

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

Database Migrations:

```
$ pip install alembic
```

Process manager to reload app automatically
```
$ pip install gunicorn httptools uvloop
```

Testing package
```
$ pip install pytest
$ pytest -v -s
```

Run the app from root directory:

```
$ uvicorn app.main:app --reload
```

### Load API
```
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run app in production
```
alembic upgrade head
pip install -r requirements.txt
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Run Docker
```
docker-compose -f docker-compose-dev.yml up -d
```
