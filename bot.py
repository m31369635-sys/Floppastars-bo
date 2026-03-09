# =====================================
# ТЕЛЕГРАМ БОТ - FloppaStars ПРАНК
# =====================================

TOKEN = "8020098998:AAE8TpMt31Wfs1uF6QXKaBDsoiLFmV43cDM"

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import random
from datetime import datetime, timedelta

bot = Bot(token=TOKEN)
dp = Dispatcher()

# База данных в памяти
users = {}  # {user_id: {"floppas": 0.0, "click_power": 0.1, "clicks": 0}}

# =====================================
# КОМАНДА /start
# =====================================
@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    
    # Регистрируем нового пользователя
    if user_id not in users:
        users[user_id] = {
            "floppas": 0.0,
            "click_power": 0.1,
            "clicks": 0
        }
    
    text = """
😸 Добро пожаловать во FloppaStars! 🐈⭐️

💰 Зарабатывай FLOPPA монеты!

👇 КЛИКАЙ НА КОТА 👇
Каждый клик дает +0.10 FLOPPA

📦 Команды:
/click - кликнуть на кота
/case - открыть кейс
/upgrade - улучшить клик
/balance - мой баланс

🚀 VIP КЕЙСЫ ЗА STARS!
Только там может выпасть NFT SNOOPDOG!
"""
    await message.answer(text)

# =====================================
# КЛИК НА КОТА
# =====================================
@dp.message(Command('click'))
async def click_cat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "click_power": 0.1, "clicks": 0}
    
    # Добавляем флоппы
    users[user_id]["floppas"] += users[user_id]["click_power"]
    users[user_id]["clicks"] += 1
    
    # Круглый счет до 2 знаков
    balance = round(users[user_id]["floppas"], 2)
    
    # Клавиатура с котом
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 КЛИК!", callback_data="click")]
    ])
    
    await message.answer(
        f"😺 **ТЫ КЛИКНУЛ КОТА!**\n\n"
        f"+{users[user_id]['click_power']} FLOPPA\n"
        f"💰 Баланс: {balance} FLOPPA\n"
        f"📊 Всего кликов: {users[user_id]['clicks']}",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "click")
async def process_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    users[user_id]["floppas"] += users[user_id]["click_power"]
    users[user_id]["clicks"] += 1
    balance = round(users[user_id]["floppas"], 2)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 КЛИК!", callback_data="click")]
    ])
    
    await callback.message.edit_text(
        f"😺 **ТЫ КЛИКНУЛ КОТА!**\n\n"
        f"+{users[user_id]['click_power']} FLOPPA\n"
        f"💰 Баланс: {balance} FLOPPA\n"
        f"📊 Всего кликов: {users[user_id]['clicks']}",
        reply_markup=keyboard
    )
    await callback.answer()

# =====================================
# ВЫБОР КЕЙСА
# =====================================
@dp.message(Command('case'))
async def case_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📦 КЕЙС ЗА FLOPPA (50 🪙)", callback_data="case_floppa")],
        [InlineKeyboardButton(text="⭐️ VIP КЕЙС (10 ⭐️)", callback_data="case_stars")]
    ])
    
    await message.answer(
        "🎁 **ВЫБЕРИ КЕЙС:**\n\n"
        "📦 Обычный кейс - 50 FLOPPA\n"
        "   Шанс на выигрыш: **0%**\n\n"
        "⭐️ VIP кейс - 10 Telegram Stars\n"
        "   🎨 NFT SNOOPDOG - ШАНС 0%\n"
        "   ❌ Пусто - ШАНС 100%\n"
        "   (Покупается за реальные деньги!)",
        reply_markup=keyboard
    )

# =====================================
# ОБЫЧНЫЙ КЕЙС (50 FLOPPA)
# =====================================
@dp.callback_query(lambda c: c.data == "case_floppa")
async def open_floppa_case(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    price = 50
    
    if users[user_id]["floppas"] < price:
        await callback.message.edit_text("❌ Недостаточно FLOPPA! Больше кликай!")
        return
    
    # Списываем флоппы
    users[user_id]["floppas"] -= price
    
    # 100% НИЧЕГО
    result = "❌ НИЧЕГО! Попробуй еще!"
    
    # Анимация
    animation = "🎰 Крутим обычный кейс...\n❌ ❌ ❌ ❌ ❌\n\n"
    
    await callback.message.edit_text(
        f"{animation}{result}\n\n"
        f"💰 Осталось: {round(users[user_id]['floppas'], 2)} FLOPPA"
    )
    await callback.answer()

# =====================================
# VIP КЕЙС ЗА STARS (10 ⭐️)
# =====================================
@dp.callback_query(lambda c: c.data == "case_stars")
async def open_stars_case(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    # Анимация VIP крутки
    animation = "⭐️ VIP КЕЙС (10 STARS) ⭐️\n\n"
    animation += "🎰 Крутим...\n"
    animation += "❌ ❌ ❌ ❌ ❌\n"
    animation += "🎨 ❌ ❌ ❌ ❌\n\n"
    
    # 100% пусто, 0% NFT
    result = "❌ **НИЧЕГО НЕ ВЫПАЛО!**\n"
    result += "🎨 NFT SNOOPDOG даже не показался...\n\n"
    result += "Повезет в следующий раз! 🍀"
    
    await callback.message.edit_text(
        f"{animation}{result}"
    )
    await callback.answer()

# =====================================
# УЛУЧШЕНИЯ
# =====================================
@dp.message(Command('upgrade'))
async def upgrade(message: types.Message):
    user_id = message.from_user.id
    current_power = users[user_id]["click_power"]
    next_power = round(current_power + 0.02, 2)
    price = int(current_power * 1000)  # Цена растет
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"⬆️ УЛУЧШИТЬ ({price} FLOPPA)", callback_data="upgrade")]
    ])
    
    await message.answer(
        f"🔧 **МАГАЗИН УЛУЧШЕНИЙ**\n\n"
        f"Текущий клик: +{current_power} FLOPPA\n"
        f"Следующий уровень: +{next_power} FLOPPA\n"
        f"Цена: {price} FLOPPA",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "upgrade")
async def process_upgrade(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_power = users[user_id]["click_power"]
    price = int(current_power * 1000)
    
    if users[user_id]["floppas"] < price:
        await callback.answer("❌ Недостаточно FLOPPA!", show_alert=True)
        return
    
    # Списываем деньги
    users[user_id]["floppas"] -= price
    # Улучшаем клик
    users[user_id]["click_power"] = round(current_power + 0.02, 2)
    
    await callback.message.edit_text(
        f"✅ **УЛУЧШЕНО!**\n\n"
        f"Теперь клик дает +{users[user_id]['click_power']} FLOPPA\n"
        f"💰 Баланс: {round(users[user_id]['floppas'], 2)} FLOPPA"
    )
    await callback.answer()

# =====================================
# БАЛАНС
# =====================================
@dp.message(Command('balance'))
async def balance(message: types.Message):
    user_id = message.from_user.id
    
    await message.answer(
        f"💰 **ТВОЙ БАЛАНС**\n\n"
        f"FLOPPA: {round(users[user_id]['floppas'], 2)}\n"
        f"Кликов: {users[user_id]['clicks']}\n"
        f"Сила клика: +{users[user_id]['click_power']}"
    )

# =====================================
# ЗАПУСК
# =====================================
async def main():
    print("=" * 40)
    print("😸 FloppaStars ПРАНК БОТ")
    print("=" * 40)
    print("✅ Бот запущен!")
    print("📦 Обычный кейс: 50 FLOPPA - 0%")
    print("⭐️ VIP кейс: 10 Stars - 100% пусто")
    print("🎨 NFT SNOOPDOG: только в VIP, шанс 0%")
    print("💰 Кликай на кота!")
    print("=" * 40)
    
    await dp.start_polling(bot)

asyncio.run(main())
