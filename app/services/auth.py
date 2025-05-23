from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from ..utils.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str):
    """Retrieve a user from the database by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user from the database by ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    """Create a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user by email and password."""
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
