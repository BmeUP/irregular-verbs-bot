from .state_interface import IState
from .db import db
from .dict_model import DictModel

class SelfInputState(IState):
    def __init__(self, message, bot, verbs: list[DictModel]) -> None:
        self.message = message
        self.bot = bot
        self.text = ""
        self.verbs = verbs
    
    def process_message(self):
        if self.message.text != "SelfInput":
            self.find_verb()
        else:
            self.hello_message()
    
    def check_every_posible_option(self, word):
        for obj in self.verbs:
            if obj.first_form == word:
                return obj
            elif obj.second_form == word:
                return obj
            elif obj.third_form == word:
                return obj

        return None
    
    def find_verb(self):
        word = f"{self.message.text.lower()}"
        self.data = self.check_every_posible_option(word)
        
        print(self.data)
        if self.data is not None:
            self.generate_message()
        else:
            self.verb_not_found_message()
            
        self.send_message()
    
    def generate_message(self):
        self.text += f"First form is  {self.generate_link(self.data.first_form)}\n"
        self.text += f"Second form is {self.generate_link(self.data.second_form)}\n"
        self.text += f"Third form is {self.generate_link(self.data.third_form)}\n"
        self.text += f"`Description: {self.data.description}`"
    
    def replace_characters(self, verb):
        return verb.replace("(", "\(").replace(")", "\)")

    def generate_link(self, verb):
        return f"[{verb}](https://dictionary.cambridge.org/dictionary/english-russian/{verb})"

    def verb_not_found_message(self):
        self.text = f"There is no irregular verb like {self.message.text}"

    def send_message(self):
        self.bot.send_message(self.message.chat.id, self.text, parse_mode="MarkdownV2")

    def hello_message(self):
        self.text = "Send me the verb\!"
        self.send_message()