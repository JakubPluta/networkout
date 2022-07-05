from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import group as group_crud
from fastapi import status, HTTPException
from backend.model.user import User, Group
from backend.security.auth import (
    get_current_user,
    check_if_current_user_is_group_owner,
    check_if_is_superuser,
)
from typing import List, Optional
from backend.crud import user as user_crud


router = APIRouter()


@router.get("/", response_model=schemas.GroupList, status_code=status.HTTP_200_OK)
def fetch_all_groups(db: Session = Depends(get_db)) -> dict:
    results = group_crud.get_all_groups(db)
    return {"results": results or []}


@router.get(
    "/{group_id}", response_model=schemas.GroupList, status_code=status.HTTP_200_OK
)
def fetch_group(group_id: int, db: Session = Depends(get_db)):
    grp = group_crud.get_group_by_id(db, group_id)
    if not grp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )
    return grp


@router.get(
    "/{group_name}/name",
    response_model=schemas.GroupWithUsers,
    status_code=status.HTTP_200_OK,
)
def fetch_group(group_name: str, db: Session = Depends(get_db)):
    grp = group_crud.get_group_by_name(db, group_name)
    if not grp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with name {group_name} not found",
        )
    return grp


@router.post("/", response_model=schemas.GroupDB, status_code=status.HTTP_201_CREATED)
def create_group(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    group: schemas.GroupCreate,
):
    grp = group_crud.get_group_by_name(db, group.name)
    if grp is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with name {group.name} already exists in database",
        )
    return group_crud.create_group(db, group, current_user.id)


@router.delete(
    "/{group_id}", response_model=schemas.GroupDB, status_code=status.HTTP_200_OK
)
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    grp = group_crud.get_group_by_id(db, group_id)
    if not grp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )
    if current_user.id == grp.created_by_id or current_user.is_superuser:
        group_crud.delete_group(db, grp)

        return {"msg": f"Group with id: {group_id} was successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You don't have permission to delete group with id {group_id}",
    )


@router.put("/{group_id}/add/{user_id}")
def add_user_to_group(
    *,
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    group_owner: bool = Depends(check_if_current_user_is_group_owner),
    is_superuser=Depends(check_if_is_superuser),
):

    if group_owner is True or is_superuser is True:

        usr = user_crud.get_user(db, user_id)
        if usr is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found",
            )

        if group_crud.is_user_in_group(db, usr, group_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with id {user_id} already belongs to group {group_id}",
            )
        try:
            group = group_crud.add_user_to_group(db, usr, group_id)
            return group
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id } doesn't exists",
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You need to be group creator or superuser to add users to group",
    )


@router.put("/{group_id}/remove/{user_id}")
def remove_user_from_group(
    *,
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    is_superuser: bool = Depends(check_if_is_superuser),
    group_owner: bool = Depends(check_if_current_user_is_group_owner),
):
    if group_owner is False or is_superuser is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be group creator or superuser to add users to group",
        )
    group = group_crud.get_group_by_id(db, group_id)

    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )

    usr = user_crud.get_user(db, user_id)
    if usr is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    try:
        group = group_crud.remove_user_from_group(db, usr, gr)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {user_id} doesn't belong to group {group_ud}",
        )
    return group
