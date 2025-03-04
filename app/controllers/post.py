from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.post import PostCreate, PostResponse
from ..services.post import create_post, get_user_posts, delete_post
from ..middlewares.auth import get_current_user
from ..models.user import User

router = APIRouter(tags=["posts"])


@router.post("/posts", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_post(post: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new post for the current user."""
    db_post = create_post(db, post, current_user.id)
    return {"postID": db_post.id}


@router.get("/posts", response_model=List[PostResponse])
def get_posts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all posts for the current user."""
    posts = get_user_posts(db, current_user.id)
    return posts


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a specific post if owned by the current user."""
    success = delete_post(db, post_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found or not owned by you"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
