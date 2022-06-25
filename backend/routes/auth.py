from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.security import auth
from typing import Any
from fastapi import status, HTTPException
from backend.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordRequestForm
from backend.model.user import User
from backend.security.auth import get_current_user

router = APIRouter()


@router.post('/login', summary="Create access and refresh tokens for user", status_code=status.HTTP_200_OK)
def login(*, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    usr = auth.authenticate(email=form_data.username, password=form_data.password, db=db)
    return {
        'access_token': auth.encode_jwt_token(user_id=str(usr.id)),
        'token_type': 'bearer'
    }


@router.get('/me', response_model=schemas.UserFromDB)
def read_current_user(current_user: User = Depends(get_current_user)) -> Any:
    return current_user
