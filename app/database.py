from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# connecting to the database
# while True:
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='nullbr', password='bmw123', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("[INFO] Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connection to the database failed.")
#         print("[WARN]", error)
#         time.sleep(2)

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://nullbr:bmw123@localhost/fastapi'

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