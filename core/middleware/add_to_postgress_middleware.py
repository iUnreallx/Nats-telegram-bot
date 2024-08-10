
from typing import Any, Awaitable, Callable, cast, Optional

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest, TelegramMigrateToChat
from aiogram.types import TelegramObject, Update, Message
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.database.postgres_connect import User


async def db_register_user(message: Message, session: AsyncSession) -> bool:
    user_id: Optional[int, None] = message.from_user.id
    username: Optional[str, None] = message.from_user.username
    fullname: Optional[str | None] = message.from_user.full_name

    user = User(user_id=user_id, username=username, fullname=fullname)
    session.add(user)
    await session.commit()

async def update_user_info(message: Message, session: AsyncSession) -> bool:
    user_id: Optional[int, None] = message.from_user.id
    username: Optional[str, None] = message.from_user.username
    fullname: str = message.from_user.full_name

    user = await session.execute(select(User).filter_by(user_id=user_id))
    user = user.scalar()

    if user:
        values_to_update = {}
        if username:
            values_to_update['username'] = username
        if fullname:
            values_to_update['fullname'] = fullname

        await session.execute(update(User).where(User.user_id==user_id).values(values_to_update))
        await session.commit()

class AddToPostgresMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event = cast(Update, event)

        async with self.session_pool() as session:
            try:
                user_id = None
                if event.message and event.message.from_user:
                    user_id = event.message.from_user.id

                UserDB = await session.execute(select(User).filter_by(user_id=user_id))
                UserDB = UserDB.fetchone()

                if event.message:
                    if not UserDB:
                        await db_register_user(event.message, session)
                    else:
                        await update_user_info(event.message, session)
                return await handler(event, data)

            except (TelegramForbiddenError, TelegramBadRequest, TelegramMigrateToChat) as e:
                print(e)