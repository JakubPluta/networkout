from fastapi import APIRouter
from backend import schemas
from backend.database.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.crud import user as user_crud
from fastapi import status, HTTPException
from backend.model.user import User
from backend.security.auth import get_current_user, get_current_superuser
from backend.crud import role as role_crud
from backend.utils.exc import FriendshipException

router = APIRouter()


@router.get("/", response_model=schemas.UsersList, status_code=status.HTTP_200_OK)
def fetch_all_users(db: Session = Depends(get_db)) -> dict:
    results = user_crud.get_all_users(db)
    return {"results": results or []}


@router.get(
    "/{user_id}", response_model=schemas.UserFromDB, status_code=status.HTTP_200_OK
)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


@router.put(
    "/{user_id}", response_model=schemas.UserFromDB, status_code=status.HTTP_201_CREATED
)
def update_user(
    *,
    current_user: User = Depends(get_current_user),
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
):
    updated_user = user_crud.update_user(db, current_user, user)
    return updated_user


@router.delete(
    "/{user_id}", response_model=schemas.UserFromDB, status_code=status.HTTP_200_OK
)
def delete_user(
    *,
    current_user: User = Depends(get_current_user),
    user_id: int,
    db: Session = Depends(get_db),
):
    if not user_crud.is_superuser(db, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be superuser to delete users",
        )
    to_delete = user_crud.get_user(db, user_id)
    if not to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    deleted = user_crud.delete_user(db, to_delete)
    if deleted:
        return {"msg": f"user wit id {user_id} successfully deleted"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong, user was not deleted.",
    )


@router.put(
    "/{user_id}/grant-superuser",
    response_model=schemas.UserFromDB,
    status_code=status.HTTP_201_CREATED,
)
def grant_users_permission(
    *,
    current_user: User = Depends(get_current_superuser),
    user: schemas.UserSuperUserUpdate,
    db: Session = Depends(get_db),
):
    updated_user = user_crud.grant_superuser_permissions(db, current_user, user)
    return updated_user


@router.get("/{user_id}/superuser", status_code=status.HTTP_201_CREATED)
def fetch_if_is_superuser(*, user_id: int, db: Session = Depends(get_db)) -> dict:
    user = user_crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return {
        "msg": f"User: {user.username} ({user.email}) {'is' if user.is_superuser else 'is not'} superuser"
    }


@router.put(
    "/befriend/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserWithFriends,
)
def befriend(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    other_user_id: int,
):
    other_user = user_crud.get_user(db=db, user_id=other_user_id)
    if other_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {other_user_id} not found",
        )
    try:
        user = user_crud.become_friend_with_user(db, current_user, other_user)
    except FriendshipException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}"
        ) from e
    return user


@router.put(
    "/unfriend/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserWithFriends,
)
def unfriend(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    other_user_id: int,
):
    other_user = user_crud.get_user(db=db, user_id=other_user_id)
    if other_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {other_user_id} not found",
        )
    try:
        user = user_crud.unfriend_with_user(db, current_user, other_user)
    except FriendshipException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}"
        ) from e
    return user


@router.get(
    "/friends/", status_code=status.HTTP_201_CREATED, response_model=schemas.Friends
)
def fetch_my_friends(*, current_user: User = Depends(get_current_user)):
    friends = user_crud.get_my_friends(current_user)
    return {"results": friends}


@router.get(
    "/{user_id}/friends/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Friends,
)
def get_user_friends(
    *,
    user_id: int,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    user = user_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return {"results": user_crud.get_my_friends(user)}
