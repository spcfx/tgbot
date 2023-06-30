import logging
logging.basicConfig()

import os
from typing import Tuple

from dotenv import load_dotenv
from src.handlers import (
    test_handler,
    search_handler,
)
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import UnauthorizedError


# Load  keys
def load_keys() -> Tuple[str, int, str]:
    load_dotenv()
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOTTOKEN")
    return api_id, api_hash, bot_token


async def bot() -> None:
    while True:
        api_id, api_hash, bot_token = load_keys()
        try:
            client = await TelegramClient(None, api_id, api_hash).start(
                bot_token=bot_token
            )
            logging.info("Successfully initiate bot")
        except UnauthorizedError:
            logging.error(
                "Unauthorized access. Please check your Telethon API ID, API hash"
            )
        except Exception as e:
            logging.error(f"Error occurred: {e}")

        # Search feature
        client.add_event_handler(search_handler)

        # Terminal bash feature
        client.add_event_handler(test_handler)

        print("Bot is running")
        await client.run_until_disconnected()
