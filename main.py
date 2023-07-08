import os
import subprocess

from aiogram import Dispatcher, Bot, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, BufferedInputFile
from dotenv import load_dotenv

load_dotenv()

dp = Dispatcher()
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"), parse_mode="HTML")
chat_id = int(os.getenv("TELEGRAM_CHAT_ID"))


@dp.message(F.text.startswith("/update_dev_frontend"))
async def update_frontend(message: Message):
    if message.chat.id != chat_id:
        return

    m = await message.reply("Команда выполняется...")
    result = os.popen(os.getenv("UPDATE_FRONTEND_CMD")).read()
    try:
        await m.edit_text(f"Команда выполнена: <code>{result}</code>")
    except TelegramBadRequest:
        await m.delete()
        await message.reply_document(document=BufferedInputFile(result.encode("utf-8"), filename="output.txt"),
                                     caption="Команда выполнена")


@dp.message(F.text.startswith("/update_dev_backend"))
async def update_backend(message: Message):
    if message.chat.id != chat_id:
        return

    m = await message.reply("Команда выполняется...")
    result = os.popen(os.getenv("UPDATE_BACKEND_CMD")).read()
    try:
        await m.edit_text(f"Команда выполнена: <code>{result}</code>")
    except TelegramBadRequest:
        await m.delete()
        await message.reply_document(document=BufferedInputFile(result.encode("utf-8"), filename="output.txt"), caption="Команда выполнена")


dp.run_polling(bot)