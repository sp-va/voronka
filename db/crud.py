import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.models import User


async def get_user(async_session: async_sessionmaker[AsyncSession], user_id: int):
    async with async_session() as session:
        stmt = select(User).where(User.id==user_id)
        result = await session.execute(stmt, execution_options={"compiled_cache": None})
        user_data = result.scalars().one_or_none()
        return user_data


async def add_user(async_session: async_sessionmaker[AsyncSession], user_id: int, created_at: datetime.datetime):
    async with async_session() as session:
        async with session.begin():
            stmt = User(
                id=user_id,
                created_at=created_at,
                status_updated_at=created_at,
            )
            session.add(stmt)


async def update_status_finished(async_session: async_sessionmaker[AsyncSession], user_id: int, updated_at:datetime.datetime):
    async with async_session() as session:
        async with session.begin():
            stmt = update(User).where(User.id == user_id).values(status_updated_at=updated_at, status="finished")
            await session.execute(stmt)


async def update_status_dead(async_session: async_sessionmaker[AsyncSession], user_id: int, updated_at:datetime.datetime):
    async with async_session() as session:
        async with session.begin():
            stmt = update(User).where(User.id == user_id).values(status_updated_at=updated_at, status="dead")
            await session.execute(stmt)
