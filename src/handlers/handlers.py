import asyncio
import logging
import random

from telethon.events import NewMessage, StopPropagation, register
from telethon.tl.functions.messages import SetTypingRequest
from telethon.tl.types import SendMessageTypingAction


@register(NewMessage(pattern="/search"))
async def search_handler(event: NewMessage) -> None:
    client = event.client
    chat_id = event.chat_id
    await client(SetTypingRequest(peer=chat_id, action=SendMessageTypingAction()))
    response = "testtest"
    try:
        await client.send_message(chat_id, f"__Here is your search:__\n{response}")
        logging.info(f"Sent /search to {chat_id}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        await event.reply("**Fail to get response**")
    await client.action(chat_id, "cancel")
    raise StopPropagation


@register(NewMessage(pattern="/test"))
async def test_handler(event: NewMessage) -> None:
    client = event.client
    response = "testtest"
    try:
        await client.send_message(event.chat_id, f"{response}")
        logging.info(f"Sent /test to {event.chat_id}")
    except Exception as e:
        logging.error(f"Error occurred while responding /test cmd: {e}")
    raise StopPropagation

