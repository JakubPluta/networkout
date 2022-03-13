from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from sqlalchemy import MetaData

# TODO: Replace with postgres, add dockerfile
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db" # "postgresql://user:password@postgresserver/db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


@contextmanager
def session(engine_=engine):
    _session = Session(engine_)
    try:
        yield _session
    except Exception as e:
        print(str(e))
        _session.rollback()
        raise Exception("Could not store data - doing rollback")
    finally:
        _session.close()


meta = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta)
