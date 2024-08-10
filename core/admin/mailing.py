from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from nats.js import JetStreamContext
from nats.js.api import ConsumerInfo
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.nats_connect import connect_to_nats
from core.database.postgres_connect import User

router = Router()


@router.message(Command('admin'))
async def admin(message: Message, bot: Bot, command: CommandObject, session: AsyncSession) -> None:
    text = command.args

    users = await session.execute(select(User.user_id))
    users = users.scalars().all()

    js: JetStreamContext = await connect_to_nats()
    await bot.send_message(chat_id=message.chat.id,
                           text='ok')

    for user in users:
        check = await session.execute(select(User.send).where(User.user_id == user_id))
        check = check.scalar()

        if check != 1:
            info: ConsumerInfo = await js.consumer_info(stream='MESSAGES', consumer=f'mailing_{user}')
            sender_info = info.name
            if sender_info:
                user_id = int(sender_info.split('_')[1])
                try:
                    await bot.send_message(chat_id=user_id,
                                           text=text)
                except:
                    print('User blocked the bot.')

                await session.execute(update(User).where(User.user_id == user).values(send = 1))
                await session.commit()


@router.message(Command('clear_all'))
async def clear_all(message: Message, bot: Bot, session: AsyncSession) -> None:
    await session.execute(update(User).values(send = 0))
    await session.commit()
    await bot.send_message(chat_id=message.chat.id,
                           text='ok')