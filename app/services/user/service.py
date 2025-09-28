from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import db_session
from app.models import User


class UserService:

    @staticmethod
    async def get_user_by_tg_user_id(tg_user_id: str) -> User | None:
        async for db in db_session():
            user_record = await db.execute(
                select(User).where(User.tg_user_id == tg_user_id)
            )
            user = user_record.scalar_one_or_none()
            return user

    @staticmethod
    async def get_user_by_email(email: str) -> User | None:
        async for db in db_session():
            user_record = await db.execute(select(User).where(User.email == email))
            user = user_record.scalar_one_or_none()
            return user

    @staticmethod
    async def create_user(
        tg_user_id: str, tg_username: str, name: str, email: str
    ) -> User:
        async for db in db_session():
            user = User(
                tg_user_id=tg_user_id, tg_username=tg_username, name=name, email=email
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    @staticmethod
    async def update_user_details(
        tg_user_id: str,
        name: str | None = None,
        email: str | None = None,
    ) -> User:
        async for db in db_session():
            user_record = await db.execute(
                select(User).where(User.tg_user_id == tg_user_id)
            )
            user = user_record.scalar_one_or_none()

            if not user:
                raise ValueError("User not found")

            email_user_record = await db.execute(
                select(User).where(User.email == email)
            )
            email_exists = email_user_record.scalar_one_or_none()

            if email and email_exists and email_exists.id != user.id:
                raise ValueError("Email already in use by another user")

            if name:
                user.name = name
            if email:
                user.email = email

            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user

    @staticmethod
    async def delete_user(tg_user_id: str) -> bool:
        async for db in db_session():
            user_record = await db.execute(
                select(User).where(User.tg_user_id == tg_user_id)
            )
            user = user_record.scalar_one_or_none()

            if user:
                await db.delete(user)
                await db.commit()
                return True
            else:
                raise ValueError("User not found")

    @staticmethod
    async def get_all_users_paginated(page: int, per_page: int) -> list[User]:
        offset = (page - 1) * per_page
        async for db in db_session():
            users = await db.execute(
                select(User)
                .offset(offset)
                .limit(per_page)
                .order_by(User.created_at.desc())
            )
            return users.scalars().all()

    @staticmethod
    async def admin_update_user_role(tg_user_id: str, role: str) -> User:
        async for db in db_session():
            user_record = await db.execute(
                select(User).where(User.tg_user_id == tg_user_id)
            )
            user = user_record.scalar_one_or_none()

            if not user:
                raise ValueError("User not found")

            user.role = role

            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
