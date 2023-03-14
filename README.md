## Sales API
https://sales-api.bruno.buzz/docs

[![wakatime](https://wakatime.com/badge/user/9450441a-ff7b-4805-b841-897d35ef3820/project/8fd606a2-3b16-45f1-9fb0-12b25ac2eed6.svg)](https://wakatime.com/badge/user/9450441a-ff7b-4805-b841-897d35ef3820/project/8fd606a2-3b16-45f1-9fb0-12b25ac2eed6)

Developed a fully fledged CRUD API in Python with the FastAPI framework. Postgresql was
used forthe database, and testing with the TestClient package. The app was published to a
production Ubuntu Serverin Digital Ocean, using Nginx and Certbot.

### Dependencies

- python ~> 3.10
- pip ~> 21.3
- postgresql ~> 13

### Production set up
Production machine is ubuntu 20.04 on DigitalOcean
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
