from .state_interface import IState
from .db import db

class SelfInputState(IState):
    def __init__(self, message, bot) -> None:
        self.message = message
        self.bot = bot
    
    def process_message(self):
        self.find_verb()
    
    def find_verb(self):
        sql = """select first_form, second_form, third_form from iverbs 
                where first_form = :verb or 
                second_form = :verb or 
                third_form = :verb;"""
        self.data = db.fetch_one(sql, {"verb": f"{self.message.text} "})
        
        if self.data is not None:
            self.generate_message()
            self.send_message()
    
    def generate_message(self):
        self.text = "Here we go\!\n"
        self.text += f"First form is [{self.data[0]}](https://www.google.com/)\n"
        self.text += f"Second form is {self.data[1]}\n"
        self.text += f"Third form is {self.data[2]}\n"

    def send_message(self):
        self.bot.send_message(self.message.chat.id, self.text, parse_mode="MarkdownV2")