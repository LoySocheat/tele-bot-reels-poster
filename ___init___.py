import os,re
import telebot
import facebook_service
import video_dl_service
from dotenv import load_dotenv

load_dotenv()
user_access_tokens = {}

api_key_bot = os.getenv('TELEGRAM_API_TOKEN')
if not api_key_bot:
    print('You need to set the TELEGRAM_API_TOKEN environment variable')
    exit()

bot = telebot.TeleBot(api_key_bot)

# Helper function to remove a file
def remove_file(file_path):
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error removing file {file_path}: {str(e)}")
    
# Get title for the video
def get_title(message, access_token, video_path):
    chat_id = message.chat.id
    title = message.text

    bot.send_message(chat_id, "Enter the description for the video:")
    bot.register_next_step_handler(message, get_description, access_token, video_path, title)
    
# Get description for the video
def get_description(message, access_token, video_path, title):
    chat_id = message.chat.id 
    description = message.text

    bot.send_message(chat_id, "Uploading video to Facebook...")
    video_id = facebook_service.create_reel(access_token, video_path)
    if video_id:
        publish_response = facebook_service.publish_reel_to_page(access_token, video_id, title, description)
        if publish_response and publish_response.status_code == 200:
            bot.send_message(chat_id, "Reel published to Facebook page successfully.")
            if remove_file(video_path):
                print(f"Deleted video file {video_path}")
            else:
                print(f"Failed to delete video file {video_path}")
        else:
            bot.send_message(chat_id, "Failed to publish reel to Facebook page.")
            if remove_file(video_path):
                print(f"Deleted video file {video_path}")
            else:
                print(f"Failed to delete video file {video_path}")
    else:
        del user_access_tokens[chat_id]
        bot.send_message(chat_id, "Failed to upload video to Facebook. Session has expired")
        if remove_file(video_path):
            print(f"Deleted video file {video_path}")
        else:
            print(f"Failed to delete video file {video_path}")
        
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me your Facebook access token to get started.")
    chat_id = message.chat.id
    if chat_id in user_access_tokens:
        del user_access_tokens[chat_id]
        bot.send_message(chat_id, "Old access token cleaned.")
    
# Upload by video from Youtube
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_access_tokens:
        if facebook_service.handle_check_token(chat_id, text):
            user_access_tokens[chat_id] = text
            bot.send_message(chat_id, 'Token has been saved successfully!')
            bot.send_message(chat_id, 'Now send me the YouTube video URL you want to upload.')
        else:
            bot.send_message(chat_id, 'Invalid token. Please try again.')

    else:
        access_token = user_access_tokens[chat_id]
        youtube_url = text
        save_path = 'videos'

        if re.match(r'^https?://(?:www\.)?(?:m\.)?youtube\.com/watch\?.*v=.*', youtube_url) or re.match(r'^https?://(?:www\.)?(?:m\.)?youtube\.com/shorts/.*', youtube_url):
            downloaded_video_filename = video_dl_service.download_youtube_video(youtube_url, save_path)
            if downloaded_video_filename:
                video_path = os.path.normpath(os.path.join(save_path, os.path.basename(downloaded_video_filename)))
                bot.send_message(chat_id, "Enter the title for the video:")
                bot.register_next_step_handler(message, get_title, access_token, video_path)
            else:
                bot.send_message(chat_id, f"{youtube_url} is age restricted, and can't be accessed without logging in.", disable_web_page_preview=True)
        else:
            bot.send_message(chat_id, "Please send a valid YouTube video URL.")
bot.polling()