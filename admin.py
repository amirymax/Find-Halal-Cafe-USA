import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command

ADMIN_IDS = [5810325088, 5533441288, 1007463279]
admin_router = Router()

with open("restaurants.json", "r", encoding="utf-8") as file:
    restaurants_data = json.load(file)

def create_states_keyboard():
    buttons = [KeyboardButton(text=state) for state in restaurants_data.keys()]
    keyboard = ReplyKeyboardMarkup(keyboard=[buttons[i:i+3] for i in range(0, len(buttons), 3)], resize_keyboard=True)
    return keyboard

class NewCafe(StatesGroup):
    state = State()
    name = State()
    address = State()
    phone = State()
    delivery = State()
    description = State()

    
@admin_router.message(Command('newcafe'))
async def new_cafe(message: types.Message, state: FSMContext):
    await state.set_state(NewCafe.state)
    if message.from_user.id in ADMIN_IDS:
        await message.reply("Салом Админ! Барои иловаи кафеи нав, штатро интихоб кунед!", reply_markup=create_states_keyboard())
    else:
        await message.reply("❌ <b>У вас нет прав для использования этой команды.</b>")

@admin_router.message(NewCafe.state)
async def process_state(message: types.Message, state: FSMContext):
    await state.update_data(state=message.text)
    await state.set_state(NewCafe.name)
    await message.reply("🍽 <b>Название кафе:</b>", reply_markup=ReplyKeyboardRemove())

@admin_router.message(NewCafe.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewCafe.address)
    await message.reply("📍 <b>Адрес кафе:</b>")

@admin_router.message(NewCafe.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(NewCafe.phone)
    await message.reply("📞 <b>Номер телефона:</b>")

@admin_router.message(NewCafe.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(NewCafe.delivery)
    await message.reply("🚙 <b>Доставка:</b>")

@admin_router.message(NewCafe.delivery)
async def process_delivery(message: types.Message, state: FSMContext):
    await state.update_data(delivery=message.text)
    await state.set_state(NewCafe.description)
    await message.reply("📝 <b>Описание:</b>")

@admin_router.message(NewCafe.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    
    # Получаем данные из состояния
    data = await state.get_data()
    state = data.get("state")
    name = data.get("name")
    address = data.get("address")
    phone = data.get("phone")
    delivery = data.get("delivery")
    description = data.get("description")
    
    # Добавляем новый кафе в JSON
    restaurants_data[state].append({
        "name": name,
        "address": address,
        "phone": phone,
        "delivery": delivery,
        "description": description
    })
    with open("restaurants.json", "w", encoding="utf-8") as file:
        json.dump(restaurants_data, file, indent=4, ensure_ascii=False)

    await message.reply("🍽 <b>Кафе успешно добавлено!</b>")

    await state.finish()
    await state.clear()
