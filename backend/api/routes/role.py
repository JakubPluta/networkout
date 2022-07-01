from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import role as role_crud
from fastapi import status, HTTPException
from backend.model.user import User
from backend.security.auth import get_current_superuser
from backend.crud import user as user_crud

router = APIRouter()


@router.get('/', response_model=schemas.RolesList, status_code=status.HTTP_200_OK)
def fetch_all_roles(db: Session = Depends(get_db)) -> dict:
    results = role_crud.get_all_roles(db)
    return {'results' : results or []}


@router.get('/{role_id}', response_model=schemas.RoleDB, status_code=status.HTTP_200_OK)
def fetch_role(role_id: int, db: Session = Depends(get_db)):
    role = role_crud.get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} not found")
    return role


@router.get('/{role_name}/name', response_model=schemas.RoleDB, status_code=status.HTTP_200_OK)
def fetch_role_by_name(role_name: str, db: Session = Depends(get_db)):
    role = role_crud.get_role_by_name(db, role_name)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with name {role_name} was not found.")
    return role


@router.post('/', response_model=schemas.RoleDB, status_code=status.HTTP_201_CREATED)
def create_role(*, db: Session = Depends(get_db), superuser: User = Depends(get_current_superuser),role: schemas.RoleCreate):
    role_db = role_crud.get_role_by_name(db, role.name)
    if role_db is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with name {role.name}already exists in database")
    return role_crud.create_role(db, role)


@router.put('/{role_id}', response_model=schemas.RoleDB, status_code=status.HTTP_201_CREATED)
def update_role(*, role_id: int, db: Session = Depends(get_db), superuser: User = Depends(get_current_superuser), role: schemas.RoleUpdate):
    role_db = role_crud.get_role_by_id(db, role_id)
    if role_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} doesn't exist")
    return role_crud.update_role(db, role_db, role)


@router.delete('/{role_id}', status_code=status.HTTP_202_ACCEPTED)
def delete_role(role_id: int, db: Session = Depends(get_db), superuser: User = Depends(get_current_superuser)):
    role_db = role_crud.get_role_by_id(db, role_id)
    if role_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} doesn't exist")
    role_crud.delete_role(db, role_id)
    return {'msg' : f"Role with id:{role_id} and name: {role_db.name} successfully deleted"}


@router.put('/{user_id}/add/{role_id}',response_model=schemas.UserFromDB)
def add_role_for_user(user_id: int, role_id: int,  db: Session = Depends(get_db), superuser: User = Depends(get_current_superuser)):
    user_db = user_crud.get_user(db, user_id)
    role_db = role_crud.get_role_by_id(db, role_id)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} doesn't exist" )

    if role_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} doesn't exist")

    role_crud.add_role_to_user(db, user_db, role_id)
    return user_db


@router.get('/{role_id}/users/', response_model=schemas.RoleDBUsers)
def get_all_users_with_role(*, role_id: int, db: Session = Depends(get_db)):
    role_db = role_crud.get_role_by_id(db, role_id)
    if role_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with id {role_id} doesn't exist")
    return role_db
