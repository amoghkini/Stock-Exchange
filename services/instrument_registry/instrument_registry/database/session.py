from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from instrument_registry.config.config_manager import ConfigManager
from instrument_registry.config.config import Config

config = ConfigManager.get_config()
DB_URL = config.DATABASE_URL


# Create the SQLAlchemy engine
engine = create_engine(
    DB_URL, echo=False if ConfigManager.get_env() == Config.PROD.value else True
)

# Create a session local factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session for thread-safe session management
Session = scoped_session(SessionLocal)
