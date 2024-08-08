import os,re
import telebot
import requests
from dotenv import load_dotenv

load_dotenv()

user_access_tokens = {}
url_facebook_graph = os.getenv('URL_FACEBOOK_GRAPH')
verison_facebook_graph = os.getenv('VERISON_FACEBOOK_GRAPH')
api_key_bot = os.getenv('TELEGRAM_API_TOKEN')
if not api_key_bot:
    print('You need to set the TELEGRAM_API_TOKEN environment variable')
    exit()
    
    
def handle_check_token(chat_id, token):
    url = f'{url_facebook_graph}/{verison_facebook_graph}/me?access_token={token}'
    response = requests.get(url)
    print(response.json().get('error', {}).get('message'))
    
    if response.status_code == 200:
        user_access_tokens[chat_id] = token
        return True
    return False

bot = telebot.TeleBot(api_key_bot)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me your Facebook access token to get started.")
    chat_id = message.chat.id
    if chat_id in user_access_tokens:
        del user_access_tokens[chat_id]
        bot.send_message(chat_id, "Old access token cleaned.")
    
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_access_tokens:
        if handle_check_token(chat_id, text):
            bot.send_message(chat_id, 'Token has been saved successfully!')
            bot.send_message(chat_id, 'Now send me the YouTube video URL you want to download.')
        else:
            bot.send_message(chat_id, 'Invalid token. Please try again.')
    else:
        access_token = user_access_tokens[chat_id]
        youtube_url = text
        save_path = 'videos'
    
bot.polling()