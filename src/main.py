import asyncio
import logging
import os
import subprocess
from typing import Generator

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse

import logging
logging.basicConfig()

import os
from typing import Tuple

from src.handlers import (
    test_handler,
    search_handler,
)
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import UnauthorizedError
from config import Config

BOT_NAME="grsbot"
BOT_VERSION="0.0.1"

async def bot() -> None:
    while True:
        try:
            client = await TelegramClient(None, config.TELEGRAM_CORE_API_ID, config.TELEGRAM_CORE_API_HASH).start(
                bot_token=config.TELEGRAM_BOT_TOKEN
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


# API and app handling
app = FastAPI(
    title=BOT_NAME,
)


@app.on_event("startup")
def startup_event() -> None:
    try:
        loop = asyncio.get_event_loop()
        background_tasks = set()
        task = loop.create_task(bot())
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
    except Exception as e:
        logging.critical(f"Error occurred while starting up app: {e}")


@app.get("/")
def root() -> str:
    return f"{BOT_NAME} {BOT_VERSION} is online"


@app.get("/health")
def health_check() -> str:
    return f"{BOT_NAME} {BOT_VERSION} is online"


# Minnion run
if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8080)
    uvicorn.run(app, host=HOST, port=PORT)
