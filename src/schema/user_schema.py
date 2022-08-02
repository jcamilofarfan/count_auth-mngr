from typing import Optional
from datetime import date, datetime, time, timedelta
from pkg_resources import require
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,
        example= "email@email.com",
        description="User email"
    )
    username: str = Field(
        ...,
        example="username",
        description="User username",
        min_length=3,
        max_length=20
    )

class User(UserBase):
    id: int = Field(
        ...,
        example=1,
        description="User id",
        title="Id",
    )

class UserRegister(UserBase):
    password: str = Field(
        ...,
        example="password",
        description="User password",
        min_length=8,
        max_length=20
    )
    updated_at: Optional[datetime] = Field(
        ...,
        example=datetime.now(),
        description="User updated_at",
        title="Updated At",
    )


    created_at: Optional[datetime] = Field(
        ...,
        example=datetime.now(),
        description="User created at",
        title="Created At"
    )
    status: Optional[bool] = Field(
        ...,
        example=True,
        description="User status",
        title="Status"
    )