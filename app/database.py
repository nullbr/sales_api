from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''old db config'''
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# connecting to the database
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='user', password='pass', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("[INFO] Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connection to the database failed.")
#         print("[WARN]", error)
#         time.sleep(2)

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
