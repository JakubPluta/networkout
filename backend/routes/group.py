from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import group as group_crud
from fastapi import status, HTTPException
from backend.model.user import User, Group
from backend.security.auth import get_current_user
from typing import List, Optional

router = APIRouter()


@router.get('/', response_model=schemas.GroupList, status_code=status.HTTP_200_OK)
def fetch_all_groups(db: Session = Depends(get_db)) -> dict:
    results = group_crud.get_all_groups(db)
    return {'results' : results or []}


@router.get('/{group_id}', response_model=schemas.GroupDB, status_code=status.HTTP_200_OK)
def fetch_group(group_id: int, db: Session = Depends(get_db)):
    grp = group_crud.get_group_by_id(db, group_id)
    if not grp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with id {group_id} not found")
    return grp


@router.get('/name/{group_name}', response_model=schemas.GroupDB, status_code=status.HTTP_200_OK)
def fetch_group(group_name: str, db: Session = Depends(get_db)):
    grp = group_crud.get_group_by_name(db, group_name)
    if not grp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with name {group_name} not found")
    return grp


@router.post('/', response_model=schemas.GroupDB, status_code=status.HTTP_201_CREATED)
def create_group(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),group: schemas.GroupCreate):
    grp = group_crud.get_group_by_name(db, group.name)
    if grp is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group with name {group.name} already exists in database")
    return group_crud.create_group(db, group, current_user.id)
