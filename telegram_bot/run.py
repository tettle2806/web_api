import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from core.config import TOKEN

# Bot token can be obtained via https://t.me/BotFather

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="web app", web_app=WebAppInfo(url="https://c34d-89-236-218-10.ngrok-free.app/")
                )
            ],
        ]
    )
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=markup
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="web app", web_app=WebAppInfo(url="https://c34d-89-236-218-10.ngrok-free.app/")
                )
            ],
        ]
    )
    await message.answer(message.text, reply_markup=markup)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(
        token="6665851397:AAFb-Zu5ziQllCiu_f-Jxoku4XOPoZ6cDXc",
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
