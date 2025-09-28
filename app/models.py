from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import text, UniqueConstraint, Column, DateTime
from sqlmodel import Field, SQLModel


class UUIDModel(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )

    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )


class User(UUIDModel, TimestampModel, table=True):
    __tablename__ = "users"

    tg_user_id: str = Field(nullable=False, unique=True, index=True)
    tg_username: str = Field(nullable=False)
    name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    role: str = Field(default="user", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
