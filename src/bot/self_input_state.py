from .state_interface import IState
from .db import db

class SelfInputState(IState):
    def __init__(self, message, bot) -> None:
        self.message = message
        self.bot = bot
        self.text = ""
    
    def process_message(self):
        if self.message.text != "SelfInput":
            self.find_verb()
        else:
            self.hello_message()
    
    def find_verb(self):
        sql = """select first_form, second_form, third_form from iverbs 
                where first_form = :verb or 
                second_form = :verb or 
                third_form = :verb;"""
        self.data = db.fetch_one(sql, {"verb": f"{self.message.text.lower()} "})
        
        if self.data is not None:
            self.generate_message()
        else:
            self.verb_not_found_message()
            
        self.send_message()
    
    def generate_message(self):
        self.text += f"First form is  {self.generate_link(self.data[0])}\n"
        self.text += f"Second form is {self.generate_link(self.data[1])}\n"
        self.text += f"Third form is {self.generate_link(self.data[2])}\n"

    def generate_link(self, verb):
        return f"[{verb}](https://dictionary.cambridge.org/dictionary/english-russian/{verb})"

    def verb_not_found_message(self):
        self.text = f"There is no irregular verb like {self.message.text}"

    def send_message(self):
        self.bot.send_message(self.message.chat.id, self.text, parse_mode="MarkdownV2")
    
    def hello_message(self):
        self.text = "Send me the verb\!"
        self.send_message()