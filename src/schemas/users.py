from typing import Optional, TypeVar

from pydantic import BaseModel, EmailStr, Field

T = TypeVar('T')


class UserSchema(BaseModel):
    id: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    username: str = Field(..., json_schema_extra={"username": 'Username'}, max_length=20, min_length=3)
    email: EmailStr
    password: str


class RequestDetails(BaseModel):
    email: EmailStr
    password: str


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None

