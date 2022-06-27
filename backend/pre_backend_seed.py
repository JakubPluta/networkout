from backend.database.init_db import init_db
from backend.database.session import SessionLocal
from pathlib import Path

from alembic import command
from alembic.config import Config

ROOT = Path(__file__).resolve().parent.parent
alembic_cfg = Config(ROOT / "alembic.ini")


if __name__ == '__main__':
    command.downgrade(alembic_cfg, "base")
    db = SessionLocal()
    command.upgrade(alembic_cfg, "head")
    init_db(db)