from sqlalchemy.orm import Session
from backend.model.user import Role, User, Group
from backend.database.db import get_db
from backend.config import settings
import logging
from backend.security.hash_funcs import get_password_hash
from backend import schemas
from backend.crud import role as role_crud
from backend.crud import user as user_crud


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


ROLES = [
    schemas.RoleCreate(name='admin', description='This is administrator role'),
    schemas.RoleCreate(name='user', description='This is user role'),
    schemas.RoleCreate(name='test', description='This is test role'),
]

USERS = [
    (schemas.UserCreateAdminView(
        username=settings.FIRST_SUPERUSER_USERNAME,
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    ), 'admin'),
    (schemas.UserCreateAdminView(
        username='user',
        email='user@networkout.com',
        password='user',
        is_superuser=False,
    ), 'user'),

    (schemas.UserCreateAdminView(
        username='testuser',
        email='testuser@networkout.com',
        password='testuser',
        is_superuser=False,
    ), 'test' )
]


def init_db(db: Session):
    """create super user"""

    for role in ROLES:
        current_role = role_crud.get_role_by_name(db, role.name)
        if current_role is None:
            role_crud.create_role(db, role)

    for user, role_name in USERS:
        current_user = user_crud.get_user_by_email(db, user.email)
        user_role = role_crud.get_role_by_name(db, role_name)
        if current_user is None:
            setattr(user, 'role_id', user_role.id)
            print(user)
            user_crud.create_user_with_role(
                db, user
            )

