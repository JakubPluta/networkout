from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import user as user_crud
from fastapi import status, HTTPException
from backend.model.user import User
from backend.security.auth import get_current_user
from typing import List, Optional


router = APIRouter()


@router.post('/{user_id}', summary="Create address for given user. Only superusers have privilege to do that.")
def create_address_for_user(*, current_user: User = Depends(get_current_user), user_id: int, address: schemas.AddressCreate,  db: Session = Depends(get_db)):
    if not user_crud.is_superuser(db, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You need to be superuser to add addresses to other users")
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
    user_with_address = user_crud.create_address_for_user(db, user, address)
    return user_with_address


@router.get('/{user_id}', response_model=List[schemas.AddressFromDB])
def fetch_user_address(user_id: int, db: Session = Depends(get_db)):
    address = user_crud.get_user_address(db, user_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return address


@router.get('/{address_id}', response_model=List[schemas.AddressFromDB])
def fetch_address(address_id: int, db: Session = Depends(get_db)):
    address = user_crud.get_address_by_id(db, address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Address with id {address_id} not found")
    return address


@router.get('/me', response_model=Optional[List[schemas.AddressFromDB]])
def fetch_my_address(current_user: User = Depends(get_current_user)):
    return current_user.addresses


@router.post('/', response_model=schemas.AddressFromDB)
def create_address(*, db: Session = Depends(get_db), address: schemas.AddressCreate):
    return user_crud.create_address(db, address)

