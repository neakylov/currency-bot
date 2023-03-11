import asyncio
import handlers

from loader import dp, bot


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

    #asyncio.get_event_loop().run_until_complete(main()) - if asyncio.run() caused an error