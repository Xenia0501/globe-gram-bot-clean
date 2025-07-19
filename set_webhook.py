import os
import asyncio
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN

WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Убедись, что переменная задана в Render Environment

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    webhook_url = f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}"
    success = await bot.set_webhook(url=webhook_url)
    if success:
        print(f"✅ Вебхук установлен: {webhook_url}")
    else:
        print("❌ Ошибка при установке вебхука")

if __name__ == "__main__":
    asyncio.run(main())
