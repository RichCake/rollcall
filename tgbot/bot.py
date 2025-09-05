import os

import dotenv
import requests
import telebot

dotenv.load_dotenv()

TOKEN = os.getenv("TG_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.text.removeprefix("/start ")
    print(user_id)
    chat_id = message.chat.id
    response = requests.post(
        "http://django:8000/notifications/link_telegram_user/",
        data={"chat_id": chat_id, "id": user_id},
    )
    if response.status_code == 200:
        bot.reply_to(
            message,
            "You have been linked to your Django user account.",
        )
    else:
        bot.reply_to(
            message,
            "Failed to link your Telegram user to your Django user account.",
        )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
