import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

ADMIN_IDS = [5810325088, 5533441288, 1007463279]
admin_router = Router()

@admin_router.message(Command('newcafe'))
async def new_cafe(message: types.Message):
    if message.from_user.id in ADMIN_IDS:
        await message.reply("Hi, its ADmin Panel")

