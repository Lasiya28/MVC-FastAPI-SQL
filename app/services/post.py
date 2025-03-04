from sqlalchemy.orm import Session
from typing import List
import time
from ..models.post import Post
from ..models.user import User
from ..schemas.post import PostCreate

"""Simple in-memory cache"""
cache = {}
cache_ttl = 300  # 5 minutes in seconds


def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(text=post.text, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    """ Invalidate cache for this user"""
    if user_id in cache:
        del cache[user_id]

    return db_post


def get_user_posts(db: Session, user_id: int):
    """Check if data is in cache and not expired"""
    cache_key = f"user_posts_{user_id}"
    current_time = time.time()

    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if current_time - timestamp < cache_ttl:
            return cached_data

    """If not in cache or expired, fetch from DB"""
    posts = db.query(Post).filter(Post.user_id == user_id).all()

    # Update cache
    cache[cache_key] = (posts, current_time)

    return posts


def delete_post(db: Session, post_id: int, user_id: int):
    post = db.query(Post).filter(Post.id == post_id,
                                 Post.user_id == user_id).first()
    if post:
        db.delete(post)
        db.commit()

        """Invalidate cache for this user"""
        cache_key = f"user_posts_{user_id}"
        if cache_key in cache:
            del cache[cache_key]

        return True
    return False
