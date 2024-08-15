import instaloader
import telebot
import io
import requests
from PIL import Image


bot_token = "7473288815:AAEkippnUndhlgI2S3Ms_75pFgw_dpiRo4c"
bot = telebot.TeleBot(bot_token)


L = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Please enter the Instagram username")

@bot.message_handler(func=lambda message: True)
def download_and_send_profile_pic(message):
    username = message.text.strip()
    
    try:
        
        profile = instaloader.Profile.from_username(L.context, username)
        
        
        profile_pic_url = profile.profile_pic_url
        profile_pic_response = requests.get(profile_pic_url, stream=True)
        profile_pic_response.raise_for_status()
        
        
        image = Image.open(profile_pic_response.raw)
        byte_array = io.BytesIO()
        image.save(byte_array, format='JPEG')
        byte_array.seek(0)
        
        
        bot.send_photo(message.chat.id, byte_array)
    
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


bot.polling()