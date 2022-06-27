from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from backend.config import settings
from fastapi import status
from typing import Optional
from backend.model.user import User
from sqlalchemy.orm import Session
from backend.crud import user as user_crud
from backend.security.hash_funcs import verify_password
from backend.database.db import get_db
from backend.schemas.auth import TokenData


CredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def encode_jwt_token(user_id: str) -> str:
    payload = {
        'exp' : datetime.utcnow() + timedelta(days=0, minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat" : datetime.utcnow(),
        "scope" : "access_token",
        "sub" : user_id
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def authenticate(*, email: str, password: str, db: Session) -> Optional[User]:
    user = user_crud.get_user_by_email(email=email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found.")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Incorrect email or password")
    return user


def get_current_user(*, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={'verify_aud' : False}
        )

        user_id = payload.get('sub')

        if user_id is None:
            raise CredentialsException
        token_data = TokenData(user_id=user_id)

    except jwt.JWTError as e:
        raise CredentialsException

    user = user_crud.get_user(db=db, user_id=int(token_data.user_id))
    if user is None:
        raise CredentialsException
    return user


def get_current_superuser(*, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    if not user_crud.is_superuser(db, current_user.id):  # 2
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
