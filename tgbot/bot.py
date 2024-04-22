import requests
import telebot

bot = telebot.TeleBot('6343049026:AAEQPW31DKskuXe-HYgpd_ZzIMgm3mseVtw')

# def get_csrf_token():
#     response = requests.get('http://127.0.0.1:8000/notifications/get_csrf_token/')
#     if response.status_code == 200:
#         return response.json()['csrf_token']
#     return None

# def send_post_request(url, data):
#     csrf_token = get_csrf_token()
#     if csrf_token:
#         data['csrfmiddlewaretoken'] = csrf_token
#         return requests.post(url, data=data)
#     return None

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Please enter your username.')
    bot.register_next_step_handler(message, save_username)

def save_username(message):
    username = message.text
    chat_id = message.chat.id
    response = requests.post('http://127.0.0.1:8000/notifications/link_telegram_user/', data={'chat_id': chat_id, 'username': username})
    print(response.status_code)
    if response.status_code == 200:
        bot.reply_to(message, 'You have been linked to your Django user account.')
    else:
        bot.reply_to(message, 'Failed to link your Telegram user to your Django user account.')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()