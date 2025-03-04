from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.security import decode_token
from ..services.auth import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
"""OAuth2 password bearer scheme for authentication"""


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Retrieves the current user based on the JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = decode_token(token)
    if token_data is None:
        raise credentials_exception

    user = get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception

    return user
