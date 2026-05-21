from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from typing import Annotated
from fastapi import Depends

import os
from dotenv import load_dotenv

load_dotenv()
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_IP = os.environ.get('DB_IP')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_IP}:{DB_PORT}/{DB_NAME}"
engine = create_engine(url)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

