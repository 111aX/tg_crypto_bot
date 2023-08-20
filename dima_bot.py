import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6534133749:AAFYP0OYnkL7l99HRuGVV0J_dcxJ3En1tyE')

chat_id_dima = 'https://t.me/dmitriikesha'

bot.send_message(chat_id_dima, 'Privet Dimas!')

keyboard = InlineKeyboardMarkup() 
keyboard.add(InlineKeyboardButton('Option 1', callback_data = 'option1')) 
keyboard.add(InlineKeyboardButton('Option 2', callback_data = 'option2')) 

bot.send_message(chat_id_dima, 'Please select an option:', reply_markup = keyboard)
