"""
Database Configuration.

This module sets up the SQLAlchemy engine, session factory, and base class for models.
It also configures the database timezone and provides a dependency for getting database sessions.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)

# Set timezone for MySQL connections from config
@event.listens_for(engine, "connect")
def set_mysql_timezone(dbapi_conn, connection_record):
    """
    Event listener to set the MySQL session timezone upon connection.
    
    Args:
        dbapi_conn: The raw DBAPI connection object.
        connection_record: The SQLAlchemy connection record.
    """
    cursor = dbapi_conn.cursor()
    cursor.execute(f"SET time_zone='{settings.timezone}'")
    cursor.close()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

def get_db():
    """
    Database session dependency for FastAPI routes.
    
    Yields:
        Session: A SQLAlchemy database session.
        
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
