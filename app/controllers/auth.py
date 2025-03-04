from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..database import get_db
from ..schemas.user import UserCreate, UserResponse
from ..schemas.token import Token
from ..services.auth import get_user_by_email, create_user, authenticate_user
from ..utils.security import create_access_token
from ..config import settings

router = APIRouter(tags=["authentication"])


@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.

    Args:
        user (UserCreate): User data for registration.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        Token: JWT token for the new user.

    Raises:
        HTTPException:
            - 400 Bad Request: If the email is already registered.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = create_user(db, user)

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): User credentials. Defaults to Depends().
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        Token: JWT token for the authenticated user.

    Raises:
        HTTPException:
            - 401 Unauthorized: If the email or password is incorrect.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
