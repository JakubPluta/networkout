from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import role as role_crud
from fastapi import status, HTTPException
from backend.model.user import User
from backend.security.auth import get_current_superuser


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


@router.post('/', response_model=schemas.RoleDB, status_code=status.HTTP_201_CREATED)
def create_role(*, db: Session = Depends(get_db), superuser: User = Depends(get_current_superuser),role: schemas.RoleCreate):
    is_in_db = role_crud.get_role_by_name(db, role.name)
    if is_in_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Role with name {role.name}already exists in database")
    return role_crud.create_role(db, role)