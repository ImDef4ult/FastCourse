from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB = 'sqlite:///./blog.db'
engine = create_engine(SQLALCHEMY_DB, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False)
Base = declarative_base()
