import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from aiogram.client.default import DefaultBotProperties
import logging

BOT_TOKEN = "8085459493:AAGXpuo_zga_PvJ0tBs7cRmzvg0ABaAOTYc"

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


# 🎛 Клавиатура
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍦 Мороженое"),
            KeyboardButton(text="🛒 Корзина"),
        ],
        [
            KeyboardButton(text="ℹ️ О нас"),
            KeyboardButton(text="🕓 Заказы"),
        ],
    ],
    resize_keyboard=True
)

# 🔘 Обработчик /start
@dp.message(lambda message: message.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Добро пожаловать в бот-магазин мороженого! 🍨\nВыберите опцию:",
        reply_markup=main_kb
    )
    

# 🛒 Корзина
cart = {}



# 📥 Обработка нажатий кнопок
ice_cream_list = [
    {"name": "Ванильное", "id": "vanilla"},
    {"name": "Шоколадное", "id": "chocolate"},
    {"name": "Клубничное", "id": "strawberry"},
]
# Обработчик кнопки "🍦 Мороженое"
@dp.message(lambda message: message.text == "🍦 Мороженое")
async def show_ice_cream(message: Message):
    for item in ice_cream_list:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ В корзину", callback_data=f"add_{item['id']}")]
        ])
        await message.answer(f"<b>{item['name']}</b>", reply_markup=keyboard)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="🍦 Мороженое")],
        [KeyboardButton(text="🛒 Корзина")],
    ])
    await message.answer("Добро пожаловать! Выберите категорию:", reply_markup=keyboard)
    
@dp.callback_query(lambda callback: callback.data.startswith("add_"))
async def add_to_cart(callback: CallbackQuery):
    ice_cream_id = callback.data.replace("add_", "")
    name = next((i["name"] for i in ice_cream_list if i["id"] == ice_cream_id), None)
    
    user_id = callback.from_user.id
    cart.setdefault(user_id, []).append(name)
    
    await callback.answer(f"✅ {name} добавлено в корзину!")



# 🔄 Обработка нажатий по Inline-кнопкам

@dp.message(lambda message: message.text == "🛒 Корзина")
async def show_cart(message: Message):
    user_id = message.from_user.id
    items = cart.get(user_id, [])
    if items:
        text = "\n".join(f"• {item}" for item in items)
        await message.answer(f"🧺 Ваша корзина:\n{text}")
    else:
        await message.answer("🛒 Ваша корзина пуста.")



@dp.message(lambda message: message.text == "ℹ️ О нас")
async def about_handler(message: Message):
    await message.answer("Мы доставляем лучшее мороженое в городе с 2020 года! 🍧")

@dp.message(lambda message: message.text == "🕓 Заказы")
async def orders_handler(message: Message):
    await message.answer("У вас пока нет заказов.")

# ▶️ Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
