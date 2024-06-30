from sqlalchemy import create_engine, cast, String
from sqlalchemy.orm import sessionmaker, declarative_base
import pandas as pd
from utils.models import *
import streamlit as st

DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
Session=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


class SessionContextManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.session.commit()
        self.session.close()

def get_db():
    return SessionContextManager(Session)

def load_from_db():
    with get_db() as session:
        pitch_data = pd.read_sql(session.query(Pitch).statement, session.bind)
        deal_data = pd.read_sql(session.query(DealFact).statement, session.bind)
        shark_data = pd.read_sql(session.query(Shark).statement, session.bind)
        industry_data = pd.read_sql(session.query(Industry).statement, session.bind)
        location_data = pd.read_sql(session.query(Location).statement, session.bind)

    return pitch_data, deal_data, shark_data, industry_data, location_data