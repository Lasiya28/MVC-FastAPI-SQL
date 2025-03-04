from pydantic import BaseModel, Field, validator, field_validator
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    text: str = Field(..., max_length=10485760)  # 1 MB limit

    @field_validator('text')
    def validate_text_size(cls, v):
        """Validate that text is not empty"""
        if not v.strip():
            raise ValueError('Post text cannot be empty')
        """Check if text size is within 1 MB"""
        if len(v.encode('utf-8')) > 1048576:  # 1 MB in bytes
            raise ValueError('Post text exceeds 1 MB limit')
        return v


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
