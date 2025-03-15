import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Укажите ваш токен
BOT_TOKEN = "7805627856:AAEl3LjfN_Yuc-XAaCVH_rZvt_KzGiHJPgY"

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Загружаем JSON с ресторанами
with open("restaurants.json", "r", encoding="utf-8") as file:
    restaurants_data = json.load(file)

# 📍 Приветственное сообщение
WELCOME_MESSAGE = (
    "👋 <b>Добро пожаловать!</b>\n\n"
    "Этот бот поможет вам найти <b>халяльные рестораны</b> в США! 🇺🇸\n\n"
    "📌 <b>Как пользоваться:</b>\n"
    "1️⃣ Выберите нужный штат.\n"
    "2️⃣ Получите список доступных ресторанов с адресами и телефонами.\n"
    "3️⃣ Узнайте, есть ли доставка.\n\n"
    "🍽 Приятного аппетита!\n"
)

# Функция для создания клавиатуры с выбором штатов (по 3 в ряд)
def create_states_keyboard():
    buttons = [KeyboardButton(text=state) for state in restaurants_data.keys()]
    keyboard = ReplyKeyboardMarkup(keyboard=[buttons[i:i+3] for i in range(0, len(buttons), 3)], resize_keyboard=True)
    return keyboard

# 📍 Команда /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(WELCOME_MESSAGE, reply_markup=create_states_keyboard())

# 📍 Обработка выбора штата
@dp.message()
async def process_state(message: types.Message):
    state = message.text.strip()
    
    if state not in restaurants_data:
        await message.answer("❌ <b>Такого штата нет в списке!</b>\n🔍 Попробуйте выбрать из кнопок ниже.", reply_markup=create_states_keyboard())
        return
    
    restaurants = restaurants_data.get(state, [])

    if not restaurants:
        await message.answer(
            f"❌ <b>В этом штате пока нет зарегистрированных ресторанов.</b>\n"
            "🔍 Попробуйте выбрать другой штат!",
            reply_markup=create_states_keyboard()
        )
    else:
        response = f"📍 <b>Рестораны в штате {state}:</b>\n\n"
        for i, restaurant in enumerate(restaurants, start=1):
            phones = "\n📞 "+restaurant["phone"]
            response += (
                f"🍽 <b>{restaurant['name']}</b>\n"
                f"📍 <b>Адрес:</b> {restaurant['address']}\n"
                f"📞 <b>Телефон:</b> {phones}\n"
                f"🚙 <b>Доставка:</b> {restaurant['delivery']}\n"
                "➖➖➖➖➖➖➖➖➖➖\n"
            )
        await message.answer(response, reply_markup=create_states_keyboard())

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
