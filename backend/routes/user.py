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


@router.get('/', response_model=schemas.UsersList, status_code=status.HTTP_200_OK)
def fetch_all_users(db: Session = Depends(get_db)) -> dict:
    results = user_crud.get_all_users(db)
    print(results)
    return {'results' : results or []}


@router.get('/{user_id}', response_model=schemas.UserFromDB, status_code=status.HTTP_200_OK)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user


@router.put('/',  response_model=schemas.UserFromDB, status_code=status.HTTP_201_CREATED)
def update_user(*, current_user: User = Depends(get_current_user), user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_crud.update_user(db, current_user, user)
    return updated_user


@router.put('/',  response_model=schemas.UserFromDB, status_code=status.HTTP_200_OK)
def delete_user(*, current_user: User = Depends(get_current_user), user_id: int, db: Session = Depends(get_db)):
    if not user_crud.is_superuser(db, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You need to be superuser to delete users")
    to_delete = user_crud.get_user(db, user_id)
    if not to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
    deleted = user_crud.delete_user(db, to_delete)
    if deleted:
        return {'msg' : f'user wit id {user_id} successfully deleted'}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong, user was not deleted.")


@router.post('/create-address')
def create_address(*, current_user: User = Depends(get_current_user), user_id: int, address: schemas.AddressCreate,  db: Session = Depends(get_db)):
    if not user_crud.is_superuser(db, current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You need to be superuser to add addresses to other users")
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")

    user_with_address = user_crud.create_address_for_user(db, user, address)
    return user_with_address


@router.get('/{user_id}/address', response_model=List[schemas.AddressFromDB])
def fetch_user_address(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
    return user.addresses


@router.get('/my-address/', response_model=Optional[List[schemas.AddressFromDB]])
def fetch_my_address(current_user: User = Depends(get_current_user)):
    return current_user.addresses
