from backend.database.session import SessionLocal
from typing import Generator
import logging

logger = logging.getLogger(__name__)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"sql alchemy session exception occurred {str(e)}")
        db.rollback()
    finally:
        db.close()


