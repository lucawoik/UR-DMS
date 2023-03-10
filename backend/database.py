from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Insert source? (Taken from https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-parts)

# Creating database with
#   - path './backend.db'
#   - corresponding engine
#   - SessionLocal class: instances of this class will be database sessions
#   - Base class: used to create the Models

SQLALCHEMY_DATABASE_URL = "sqlite:///./backend.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
