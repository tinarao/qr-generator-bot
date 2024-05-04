import os
import asyncio
import validators
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from qr import generate

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
  await bot.reply_to(message, f"Привет, {str(message.chat.first_name)}\nЯ генерирую QR-коды. Отправь мне ссылку и я верну QR-код")
  return

@bot.message_handler(content_types=["text"])
async def send_welcome(message):
  
  if not validators.url(message.text):
    await bot.send_message(message.chat.id, "Некорректная ссылка, отправьте новую")
    return
  
  await bot.send_message(message.chat.id, "Генерирую QR-код...")
  
  code_path = generate(message.text, message.chat.id)
    
  file = open(code_path, 'rb')
  
  await bot.send_photo(message.chat.id, file)
  
  file.close()
  os.remove(code_path)
  
  await bot.send_message(message.chat.id, f"Сгенерированный QR-код, ведущий на {message.text}")
  return

def main ():
  print("Bot is running!")
  asyncio.run(bot.infinity_polling())
  
if __name__ == "__main__":
  main()