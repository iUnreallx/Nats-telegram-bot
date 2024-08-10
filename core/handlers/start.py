from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from nats.js import JetStreamContext

from core.database.nats_connect import connect_to_nats

router = Router()

@router.message(CommandStart())
async def start(message: Message, bot: Bot) -> None:
    js: JetStreamContext = await connect_to_nats()

    await js.pull_subscribe(subject=f'messages.*', durable=f'mailing_{message.from_user.id}', stream='MESSAGES')
    await bot.send_message(
        chat_id=message.chat.id,
        text='Hello')