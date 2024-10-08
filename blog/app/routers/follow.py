from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud import user_crud, post_crud
from ..models import user_models
from ..schemas import post_schemas

router = APIRouter(
    prefix='/follow',
    tags=['Follow']
)


@router.get('/', response_model=List[post_schemas.Follow])
def read_following_list_for_current_user(
        skip: int = 0, limit: int = 10,
        db: Session = Depends(get_db),
        search: Optional[str] = None,
        current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    if search:
        following_user = user_crud.get_user_by_username(db, search)
        return [post_crud.get_follow_by_user_and_following_id(
            db, following_user.id, current_user.id
        )]
    return post_crud.get_following_list(db, current_user.id, skip, limit)


@router.get('/{follow_id}/', response_model=post_schemas.Follow)
def read_single_follow(
        follow_id: int,
        db: Session = Depends(get_db),
        current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    follow = post_crud.get_single_follow(db, follow_id)
    if follow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Follow not found'
        )
    return follow


@router.post('/', response_model=post_schemas.Follow, status_code=201)
def create_follow(
        follow: post_schemas.FollowCreate,
        db: Session = Depends(get_db),
        current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    following_user = user_crud.get_user_by_username(
        db, follow.dict()['following_id']
    )
    db_follow = post_crud.get_follow_by_user_and_following_id(
        db,
        following_user.id,
        current_user.id
    )
    if db_follow:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The follow already exists'
        )
    if following_user == current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Cannot follow yuorself'
        )
    return post_crud.create_follow(db, following_user.id, current_user.id)


@router.delete('/{follow_id}/', status_code=204)
def delete_follow(
        follow_id: int,
        db: Session = Depends(get_db),
        current_user: user_models.User = Depends(user_crud.get_current_active_user)
):
    follow = post_crud.get_single_follow(db, follow_id)
    if follow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Follow not found'
        )
    if follow.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Permission denied'
        )
    return post_crud.delete_follow(db, follow)
