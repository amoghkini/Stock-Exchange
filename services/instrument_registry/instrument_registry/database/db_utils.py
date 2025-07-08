import logging

from instrument_registry.database.base_model import Base
from instrument_registry.database.session import engine


def init_db_tables():
    """
    Initializes the database by creating all tables defined by Base.metadata.
    This is typically used for initial setup in development or testing,
    not for applying migrations in production.
    """
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables initialized via create_all.")