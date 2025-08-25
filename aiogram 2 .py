from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '8359477223:AAGJhqnbcdOkN35ub0siB2u8M7DF1PoHp8c'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "👋 Привет! Я MailMuse Bot — ваш AI-ассистент по email-маркетингу.\n"
        
    )
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)