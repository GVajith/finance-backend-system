from sqlalchemy import create_engine
from config import DatabaseDetails

def get_engine():
    return create_engine(DatabaseDetails.CONNECTION_STRING)