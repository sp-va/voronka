import os
import asyncio
import datetime

from dotenv import load_dotenv

from pyrogram import Client, filters
from pyrogram.types import Message, User
from pyrogram import errors

from db.crud import get_user, add_user, update_status_finished, update_status_dead
from db.db_conn import AsyncSessionLocal

load_dotenv("../.env")

client = Client(name='userbot', api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"))

MSG1 = "msg1"
MSG2 = "msg2"
MSG3 = "msg3"


def time_for_msg2(current_time, created_at):
    diff = datetime.datetime.strptime(str(current_time), "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(created_at),
                                                                                                      "%Y-%m-%d %H:%M:%S")
    diff = diff.total_seconds()/60

    if 6 <= diff <= 39:
        return True


async def msg2_not_cancelled(user_created, user_id):
    found_messages = []
    start = user_created + datetime.timedelta(minutes=6)
    end = datetime.datetime.now()
    async for message in client.get_chat_history(user_id, limit=10):
        if start < message.date < end and message.from_user.id == user_id:
            found_messages.append(message.text)

    if len(found_messages) == 0:
        return True


@client.on_message(filters.private)
async def message_handler(user: User, message: Message):

    async def send_msg1():
        await client.send_message(message.chat.id, MSG1)

    async def send_msg2():
        await client.send_message(message.chat.id, MSG2)

    async def send_msg3():
        await client.send_message(message.chat.id, MSG3)

    try:
        user_id = message.from_user.id
        message_delivered = message.date
        user_data = await get_user(AsyncSessionLocal, user_id)

        if user_data is None:
            await add_user(AsyncSessionLocal, user_id, message_delivered)

            await asyncio.sleep(60*6) # Ожидание 6 минут для отправки msg1
            user_data = await get_user(AsyncSessionLocal, user_id)
            if not user_data.status == 'finished' and not user_data.status == 'dead':
                await send_msg1()

            await asyncio.sleep(60*39) # Ожидание 39 минут для отправки msg2
            user_data = await get_user(AsyncSessionLocal, user_id)
            msg2_allowed = await msg2_not_cancelled(user_data.created_at, user_data.id)
            if not user_data.status == 'finished' and not user_data.status == 'dead' and msg2_allowed:
                await send_msg2()

            await asyncio.sleep(60*60*26) # Ожидание 1 день и 2 часа для отправки msg3
            user_data = await get_user(AsyncSessionLocal, user_id)
            if not user_data.status == 'finished':
                await send_msg3()
                await update_status_finished(AsyncSessionLocal, user_id, datetime.datetime.now())

        user_data = await get_user(AsyncSessionLocal, user_id)

        if user_data.status == "finished" or user_data.status == "dead":
            print("Пользователь не обслуживается")

        if message.text.lower() == "прекрасно" or message.text.lower() == "ожидать":
            await update_status_finished(AsyncSessionLocal, user_id, message_delivered)
            print("Пользователь не обслуживается")

        if user_data.status != "finished" and time_for_msg2(message_delivered, user_data.created_at):
            await asyncio.sleep(10) # Ожидание 1 день и 2 часа для отправки msg3
            user_data = await get_user(AsyncSessionLocal, user_id)
            if not user_data.status == 'finished':
                await send_msg3()
                await update_status_finished(AsyncSessionLocal, user_id, message_delivered)

    except errors.UserDeactivated:
        await update_status_dead(AsyncSessionLocal, user_id, datetime.datetime.now())

client.run()
