import telebot

from .settings import settings
from .decorators import CheckUser
from .main_state import states

token = settings.bot_token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['help', 'start'])
@CheckUser()
def send_welcome(message):
    bot.reply_to(message, f"Hello {message.from_user.first_name}! I`m iVerbBot. And I know something about irregular verbs.")

@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    states.choose(message, bot)