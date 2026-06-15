#DATABASE.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
from sqlalchemy.engine import Engine
import sqlite3

# Database connection string loaded from .env
DATABASE_URL = settings.DATABASE_URL

# Create SQLAlchemy engine used to communicate with the database
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Enable SQLite foreign key constraints
# Required for ON DELETE CASCADE to work properly
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Apply only when using SQLite
    if isinstance(dbapi_connection, sqlite3.Connection):
        # Turn on foreign key support
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Factory used to create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class inherited by all database models
Base = declarative_base()

def get_db():
    """
    Provide a database session for each request.

    Opens a new session when a request starts
    and automatically closes it when finished.
    """
    # Create a new database session
    db = SessionLocal()
    try:
        # Make session available to FastAPI endpoints
        yield db
    finally:
        # Ensure database connection is closed
        db.close()