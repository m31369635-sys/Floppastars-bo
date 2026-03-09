# =====================================
# ТЕЛЕГРАМ БОТ - 😸 FloppaStars 🐈⭐️
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

last_opened = {}

# =====================================
# КОМАНДА /start
# =====================================
@dp.message(Command('start'))
async def start(message: types.Message):
    text = """
😸 Добро пожаловать во FloppaStars! 🐈⭐️

🎁 Игра с рулеткой!

Команды:
🎲 /freebox - крутить рулетку (раз в 24ч)
⏰ /time - проверить таймер
❓ /help - помощь

⚡️ Шанс на МИШУ: 1% ⚡️

Нажми /freebox чтобы крутить!
"""
    await message.answer(text)

# =====================================
# КОМАНДА /help
# =====================================
@dp.message(Command('help'))
async def help(message: types.Message):
    text = """
📋 Как играть в FloppaStars:

1. Нажимаешь /freebox
2. Появляется кнопка "🎰 КРУТИТЬ РУЛЕТКУ"
3. Нажимаешь и видишь прокрутку: ❌❌🐻❌❌
4. Если выпал МИША 🐻 - ты победил!

📊 ШАНСЫ:
• ❌ Крестик - 99%
• 🐻 Миша - 1% (редкий!)

⏳ Важно: Крутить можно раз в 24 часа!
"""
    await message.answer(text)

# =====================================
# КОМАНДА /freebox
# =====================================
@dp.message(Command('freebox'))
async def freebox(message: types.Message):
    user_id = message.from_user.id
    now = datetime.now()
    
    # Проверка времени
    if user_id in last_opened:
        diff = now - last_opened[user_id]
        if diff < timedelta(hours=24):
            remain = timedelta(hours=24) - diff
            hours = remain.seconds // 3600
            minutes = (remain.seconds % 3600) // 60
            await message.answer(
                f"⏳ **До следующей попытки:**\n"
                f"{hours} ч {minutes} мин"
            )
            return
    
    # Создаем кнопку для прокрутки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎰 КРУТИТЬ РУЛЕТКУ", callback_data="spin")]
    ])
    
    await message.answer(
        "🎁 **Рулетка FloppaStars готова!**\n"
        "Нажми кнопку чтобы крутить:",
        reply_markup=keyboard
    )

# =====================================
# ПРОКРУТКА РУЛЕТКИ
# =====================================
@dp.callback_query(lambda c: c.data == "spin")
async def spin_roulette(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    # Запоминаем время
    last_opened[user_id] = datetime.now()
    
    # Создаем рулетку из 10 символов
    symbols = []
    bear_count = 0
    
    # Генерируем 10 случайных результатов с 1% шансом на медведя
    for i in range(10):
        if random.randint(1, 100) <= 1:  # 1% шанс на Мишу!
            symbols.append("🐻")
            bear_count += 1
        else:
            symbols.append("❌")
    
    # Собираем строку для прокрутки
    spin_result = " ".join(symbols)
    
    # Определяем результат
    if bear_count >= 1:
        result_text = f"🎉 УРА! МИША! Выпало {bear_count} Миш(а)! 🐻\nЭто 1% удачи!"
    else:
        result_text = "😢 **В этот раз не повезло...**\n1% шанс на Мишу - попробуй через 24 часа!"
    
    # Отправляем результат
    await callback.message.edit_text(
        f"**😸 FloppaStars РУЛЕТКА:**\n\n"
        f"{spin_result}\n\n"
        f"{result_text}\n\n"
        f"⏰ Следующая попытка через 24 часа"
    )
    
    await callback.answer()

# =====================================
# КОМАНДА /time
# =====================================
@dp.message(Command('time'))
async def check_time(message: types.Message):
    user_id = message.from_user.id
    
    if user_id in last_opened:
        diff = datetime.now() - last_opened[user_id]
        if diff < timedelta(hours=24):
            remain = timedelta(hours=24) - diff
            hours = remain.seconds // 3600
            minutes = (remain.seconds % 3600) // 60

            await message.answer(
                f"⏳ **До следующей попытки:**\n"
                f"{hours} ч {minutes} мин"
            )
        else:
            await message.answer("✅ Можно крутить! /freebox")
    else:
        await message.answer("✅ Можно крутить! /freebox")

# =====================================
# ОСТАЛЬНЫЕ СООБЩЕНИЯ
# =====================================
@dp.message()
async def unknown(message: types.Message):
    await message.answer(
        "❓ Неизвестная команда\n"
        "Используй /start или /help"
    )

# =====================================
# ЗАПУСК
# =====================================
async def main():
    print("=" * 40)
    print("😸 FloppaStars РУЛЕТКА 🐈⭐️")
    print("=" * 40)
    print("✅ Бот @FloppaStar_Bot запущен!")
    print("🐻 Шанс на МИШУ: 1%")
    print("❌ Шанс на крестик: 99%")
    print("🎲 Рулетка: 10 символов")
    print("=" * 40)
    print("👀 Окно не закрывать!")
    print("=" * 40)
    
    await dp.start_polling(bot)

asyncio.run(main())
