import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DatabaseDetails:
    CONNECTION_STRING = f"sqlite:///{BASE_DIR}/finance.db"
    DEFAULT_SCHEMA = None