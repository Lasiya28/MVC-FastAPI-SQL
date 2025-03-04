from pydantic import BaseModel, EmailStr, Field, validator, field_validator
import re


class UserBase(BaseModel):
    email: EmailStr

    @field_validator('email')
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in v):
            raise ValueError(
                'Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError(
                'Password must contain at least one lowercase letter')
        return v


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
