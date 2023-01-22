import sqlalchemy as db
from sqlalchemy.orm import declarative_base, Session
import logging

# Databade creation
engine = db.create_engine("postgresql+psycopg2://postgres:postgres@localhost/wiki")
session = Session(engine)

Base = declarative_base()

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(msg)s')
    file_handler = logging.FileHandler('log/wikirace.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

from model import *
Base.metadata.create_all(engine)
