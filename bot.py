import asyncio 
from config import token
from aiogram import Bot, Dispatcher
from handlers import commands, personal
from rich import print
    #                       parser_mode - нужен для форматирование текста в сообщениях
    #                                               (выведет в консоль предупреждение - игнорим)
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher()
async def main():
    print("Бот запустился")
    print(bot)
    dp.include_routers(
        commands.router,
        personal.router,
        # questionaire.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__  == "__main__":
    asyncio.run(main()) 

