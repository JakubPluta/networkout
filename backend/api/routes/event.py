from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import event as event_crud
from fastapi import status, HTTPException
from backend.model.user import User, Group
from backend.security.auth import (
    get_current_user,
    check_if_current_user_is_group_owner,
    check_if_is_superuser,
)
from typing import List, Optional
from backend.crud import user as user_crud
from backend.utils.exc import EventException

router = APIRouter()


@router.get("/", response_model=schemas.EventsList, status_code=status.HTTP_200_OK)
def fetch_all_events(db: Session = Depends(get_db)) -> dict:
    results = event_crud.get_all_events(db)
    return {"results": results or []}


@router.get(
    "/{event_id}",
    response_model=schemas.EventWithParticipants,
    status_code=status.HTTP_200_OK,
)
def fetch_event(event_id: int, db: Session = Depends(get_db)):
    event = event_crud.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found",
        )
    return event


@router.get(
    "/{event_name}/name", response_model=schemas.EventDB, status_code=status.HTTP_200_OK
)
def fetch_event_by_name(event_name: str, db: Session = Depends(get_db)):
    evt = event_crud.get_event_by_name(db, event_name)
    if not evt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with name {event_name} not found",
        )
    return evt


@router.post("/", response_model=schemas.EventDB, status_code=status.HTTP_201_CREATED)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    evt = event_crud.create_event(db, event, current_user.id)
    return evt


@router.put("/{event_id}/join", status_code=status.HTTP_201_CREATED)
def join_event(
    *,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    event = event_crud.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found",
        )

    try:
        event_crud.join_event(db, current_user, event)
    except EventException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"msg": f"User {current_user.id} successfully joined to event {event_id}"}


@router.put("/{event_id}/quit", status_code=status.HTTP_201_CREATED)
def quit_event(
    *,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    event = event_crud.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found",
        )

    try:
        event_crud.quit_event(db, current_user, event)
    except EventException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"msg": f"User {current_user.id} successfully quit event {event_id}"}
