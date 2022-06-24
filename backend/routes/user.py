from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import user as user_crud
from typing import Optional, List
from fastapi import status, HTTPException

router = APIRouter()


@router.get('/', response_model=schemas.UsersList, status_code=status.HTTP_200_OK)
def fetch_all_users(db: Session = Depends(get_db)) -> dict:
    results = user_crud.get_all_users(db)
    return {'results' : results or []}


@router.post('/', response_model=schemas.UserFromDB, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(get_db), user: schemas.UserCreate):
    return user_crud.create_user(db, user)


@router.get('/{user_id}', response_model=schemas.UserFromDB, status_code=status.HTTP_200_OK)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user
