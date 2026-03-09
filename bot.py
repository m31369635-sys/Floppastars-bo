TOKEN = "8020098998:AAE8TpMt31Wfs1uF6QXKaBDsoiLFmV43cDM"

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = {}
referrals = {}
invited_count = {}

@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) > 1:
        referrer_id = int(args[1])
        if referrer_id != user_id and user_id not in referrals:
            referrals[user_id] = referrer_id
            if referrer_id in invited_count:
                invited_count[referrer_id] += 1
            else:
                invited_count[referrer_id] = 1
    
    if user_id not in users:
        users[user_id] = {
            "floppas": 0.0,
            "clicks": 0
        }
    
    invited = invited_count.get(user_id, 0)
    bot_username = (await bot.me()).username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    
    text = f"""
😸 Добро пожаловать во FloppaStars! 🐈⭐️

👇 Команды:
/click - кликнуть на кота (+0.10 FLOPPA)
/withdraw - вывести звезды (нужно 50 FLOPPA)
/balance - баланс

👥 Друзей: {invited}/2
🔗 Твоя ссылка: {ref_link}
"""
    await message.answer(text)

@dp.message(Command('click'))
async def click_cat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "clicks": 0}
    
    users[user_id]["floppas"] += 0.1
    users[user_id]["clicks"] += 1
    balance = round(users[user_id]["floppas"], 2)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 КЛИК!", callback_data="click")]
    ])
    
    await message.answer(
        f"😺 +0.10 FLOPPA\n"
        f"💰 Баланс: {balance} FLOPPA\n"
        f"📊 Кликов: {users[user_id]['clicks']}",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "click")
async def process_click(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "clicks": 0}
    
    users[user_id]["floppas"] += 0.1
    users[user_id]["clicks"] += 1
    balance = round(users[user_id]["floppas"], 2)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 КЛИК!", callback_data="click")]
    ])
    
    await callback.message.edit_text(
        f"😺 +0.10 FLOPPA\n"
        f"💰 Баланс: {balance} FLOPPA\n"
        f"📊 Кликов: {users[user_id]['clicks']}",
        reply_markup=keyboard
    )
    await callback.answer()

@dp.message(Command('balance'))
async def balance(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "clicks": 0}
    
    invited = invited_count.get(user_id, 0)
    balance = round(users[user_id]["floppas"], 2)
    
    text = f"""
💰 БАЛАНС

FLOPPA: {balance}
Кликов: {users[user_id]['clicks']}
Друзей: {invited}/2
{'✅ Можно выводить 50 FLOPPA!' if balance >= 50 and invited >= 2 else '❌ Нужно 50 FLOPPA и 2 друга'}
"""
    await message.answer(text)

@dp.message(Command('withdraw'))
async def withdraw(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "clicks": 0}
    
    invited = invited_count.get(user_id, 0)
    floppas = users[user_id]["floppas"]
    
    if invited < 2:
        await message.answer(f"❌ Нужно 2 друга! Приглашено: {invited}/2")
        return
    
    if floppas < 50:
        await message.answer(f"❌ Нужно минимум 50 FLOPPA! У тебя: {floppas}")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ ВЫВЕСТИ 50 FLOPPA", callback_data="withdraw_50")],
        [InlineKeyboardButton(text="❌ ОТМЕНА", callback_data="cancel_withdraw")]
    ])
    
    await message.answer(
        f"⭐️ ВЫВОД\n\n"
        f"Ты выведешь: 50 FLOPPA\n"f"Получишь: 50 Stars\n"
        f"Останется: {round(floppas - 50, 2)} FLOPPA\n\n"
        f"Подтверди:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "withdraw_50")
async def withdraw_50(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    users[user_id]["floppas"] -= 50
    
    await callback.message.edit_text(
        f"✅ ГОТОВО!\n\n"
        f"50 Stars скоро придут в Telegram\n"
        f"Остаток: {round(users[user_id]['floppas'], 2)} FLOPPA"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "cancel_withdraw")
async def cancel_withdraw(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Отменено")
    await callback.answer()

@dp.message()
async def unknown(message: types.Message):
    await message.answer("❓ Нажми /start")

async def main():
    print("🔥 БОТ РАБОТАЕТ!")
    print("💰 1 клик = 0.10 FLOPPA")
    print("⭐️ Вывод: 50 FLOPPA = 50 Stars")
    await dp.start_polling(bot)

asyncio.run(main())
