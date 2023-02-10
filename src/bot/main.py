import telebot
from telebot import types

from .settings import settings
from .decorators import CheckUser
from .main_state import states

token = settings.bot_token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
@CheckUser()
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    self_input_btn = types.KeyboardButton("SelfInput")
    quiz_btn = types.KeyboardButton("Quiz")
    sheet_btn = types.KeyboardButton("Gimme that sheet!")
    markup.add(self_input_btn)
    markup.add(quiz_btn)
    markup.add(sheet_btn)
    bot.send_message(message.chat.id, 
    f"Hello {message.from_user.first_name}! I`m iVerbBot. And I know something about irregular verbs.",
    reply_markup=markup)
    

@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    states.choose(message, bot)