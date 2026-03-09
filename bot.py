TOKEN = "8020098998:AAE8TpMt31Wfs1uF6QXKaBDsoiLFmV43cDM"

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import random

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
            "click_power": 0.1,
            "clicks": 0
        }
    
    bot_username = (await bot.me()).username
    ref_link = f"https://t.me/{bot_username}?start={user_id}"
    invited = invited_count.get(user_id, 0)
    
    text = f"""
😸 Добро пожаловать во FloppaStars! 🐈⭐️

👇 Доступные команды:
/click - кликнуть на кота
/withdraw - вывести FLOPPA на Stars
/balance - мой баланс

👥 Приглашено друзей: {invited}/2
🔗 Твоя ссылка: {ref_link}
"""
    await message.answer(text)

@dp.message()
async def unknown_command(message: types.Message):
    await message.answer(
        "❌ Неизвестная команда\n"
        "Нажми /start"
    )

@dp.message(Command('click'))
async def click_cat(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "click_power": 0.1, "clicks": 0}
    
    users[user_id]["floppas"] += users[user_id]["click_power"]
    users[user_id]["clicks"] += 1
    balance = round(users[user_id]["floppas"], 2)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐱 КЛИК!", callback_data="click")]
    ])
    
    await message.answer(
        f"😺 ТЫ КЛИКНУЛ КОТА!\n\n"
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
        f"😺 ТЫ КЛИКНУЛ КОТА!\n\n"
        f"+{users[user_id]['click_power']} FLOPPA\n"
        f"💰 Баланс: {balance} FLOPPA\n"
        f"📊 Всего кликов: {users[user_id]['clicks']}",
        reply_markup=keyboard
    )
    await callback.answer()

@dp.message(Command('balance'))
async def balance(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "click_power": 0.1, "clicks": 0}
    
    invited = invited_count.get(user_id, 0)
    
    await message.answer(
        f"💰 ТВОЙ БАЛАНС\n\n"
        f"FLOPPA: {round(users[user_id]['floppas'], 2)}\n"
        f"Кликов: {users[user_id]['clicks']}\n"
        f"Приглашено друзей: {invited}/2"
    )

@dp.message(Command('withdraw'))
async def withdraw(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = {"floppas": 0.0, "click_power": 0.1, "clicks": 0}
    
    invited = invited_count.get(user_id, 0)
    balance = users[user_id]["floppas"]
    
    if invited < 2:
        await message.answer(
            f"❌ Нельзя вывести!\n"
            f"Нужно пригласить 2 друзей\n"
            f"Приглашено: {invited}/2"
        )
        return
    
    if balance < 50:
        await message.answer(
            f"❌ Нельзя вывести!\n"f"Нужно минимум 50 FLOPPA\n"
            f"У тебя: {round(balance, 2)} FLOPPA"
        )
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ ПОДТВЕРДИТЬ ВЫВОД", callback_data="confirm_withdraw")],
        [InlineKeyboardButton(text="❌ ОТМЕНА", callback_data="cancel_withdraw")]
    ])
    
    await message.answer(
        f"💰 ВЫВОД НА STARS\n\n"
        f"Ты выводишь: 50 FLOPPA\n"
        f"Получишь: 1 Star\n\n"
        f"Подтверди вывод:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "confirm_withdraw")
async def confirm_withdraw(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    users[user_id]["floppas"] -= 50
    
    await callback.message.edit_text(
        "✅ ВЫВОД ОФОРМЛЕН!\n\n"
        "1 Star скоро придет тебе в Telegram\n"
        "Проверь баланс Stars в настройках"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "cancel_withdraw")
async def cancel_withdraw(callback: types.CallbackQuery):
    await callback.message.edit_text("❌ Вывод отменен")
    await callback.answer()

async def main():
    print("😸 FloppaStars БОТ ЗАПУЩЕН!")
    await dp.start_polling(bot)

asyncio.run(main())

