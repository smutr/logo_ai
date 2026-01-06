from datetime import datetime

from sqlalchemy.types import DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy import select

Base = declarative_base()
DATABASE_URL = "sqlite+aiosqlite:///logo_ai.db"
engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    free_generations_left = Column(Integer, default=1)
    paid_generations = Column(Integer, default=0)


class LogoGeneration(Base):
    __tablename__ = 'logo_generations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    prompt = Column(String, nullable=False)
    style = Column(String, nullable=False)
    url = Column(String, nullable=False)
    units = Column(Integer, nullable=False)


async def save_generation(user_id: int, prompt: str, style: str, url: str, units: int):
    async with async_session_maker() as session:
        generation = LogoGeneration(
            user_id=user_id,
            prompt=prompt,
            style=style,
            url=url,
            units=units,
        )
        session.add(generation)
        await session.commit()
        await session.refresh(generation)
        return generation


async def get_user_logos(user_id: int, limit: int = 5):
    async with async_session_maker() as session:
        result = await session.execute(
            select(LogoGeneration)
            .where(LogoGeneration.user_id == user_id)
            .order_by(LogoGeneration.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

# получение всех логотипов
async def count_user_logos(user_id: int) -> int:
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.count(LogoGeneration.id)).where(LogoGeneration.user_id == user_id)
        )
        return result.scalar_one()


async def init_db():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        # выполним создание таблиц
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def get_or_create_user(telegram_id: int, username: str):
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=telegram_id,
                username=username,
                free_generations_left=1
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user


async def try_decrement_generation(telegram_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            return None, "not_found"  # Не найден

        if user.free_generations_left > 0:
            user.free_generations_left -= 1
            await session.commit()
            await session.refresh(user)
            return user, "free"
        elif user.paid_generations > 0:
            user.paid_generations -= 1
            await session.commit()
            await session.refresh(user)
            return user, "paid"
        else:
            return user, "no_generations"


async def add_credit_user(telegram_id: int, credits: int):
    async with async_session_maker() as session:  # <-- скобки!
        # ищем пользователя
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return None  # или выбросить ошибку / вернуть статус

        # увеличиваем количество платных генераций
        user.paid_generations = (user.paid_generations or 0) + credits

        await session.commit()
        await session.refresh(user)
        return user
