from sqlalchemy.orm import Session
from backend.model.user import Role, User, Group
from backend.database.db import get_db
from backend.config import settings
import logging
from backend.security.hash_funcs import get_password_hash

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def init_db(db: Session):
    """create super user"""
    initial_roles = [
        Role(name='admin', description='Administrator'),
        Role(name='user', description='User'),
    ]

    initial_groups = [
        Group(name='users', description='Users'),
        Group(name='guests', description='Guests'),
    ]

    db.add_all([*initial_groups, *initial_roles])
    db.commit()
    logger.info("Groups and roles created")

    admin: Role = db.query(Role).filter(Role.name=='admin').first()

    if settings.FIRST_SUPERUSER_EMAIL:

        first_user = User(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            role_id = admin.id,
        )
        db.add(first_user)
        db.commit()
        logger.info(f"Super user created with email: {settings.FIRST_SUPERUSER_EMAIL}")

        for grp in db.query(Group).all():
            grp.created_by_id = db.query(User).filter(User.username == settings.FIRST_SUPERUSER_USERNAME).first().id
            db.add(grp)
            db.commit()
    logger.info("Super user not found in config file. No user created.")
