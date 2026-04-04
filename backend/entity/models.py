from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    user_code: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(nullable=False)
    profile_image: str | None = Field(nullable=True)
    email: str | None = Field(nullable=True, default=None)
    kakao_user_id: str | None = Field(nullable=False, unique_items=True)


class Category(SQLModel, table=True):
    category_code: int | None = Field(default=None, primary_key=True)
    user_code: int | None = Field(foreign_key="user.user_code")
    name: str | None = Field(nullable=False, max_length=30)


class Link(SQLModel, table=True):
    link_code: int | None = Field(default=None, primary_key=True)
    user_code: int | None = Field(foreign_key="user.user_code")
    category_code: int | None = Field(foreign_key="category.category_code")
    link: str | None = Field(nullable=False, max_length=3000)
    title: str | None = Field(nullable=False)
    created_at: datetime | None = Field(default=datetime.now(), nullable=False)
    category: Optional["Category"] = Relationship()

