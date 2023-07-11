import random

from .state_interface import IState
from .db import db
from .dict_model import DictModel

class QuizState(IState):
    def __init__(self, message, bot, verbs: list[DictModel]) -> None:
        self.message = message
        self.bot = bot
        self.text = ""
        self.user = None
        self.verbs = verbs
    
    def process_message(self):
        if self.message.text == "Quiz":
            self.get_user()
        else:
            self.check_user_answer()

        self.bot.send_message(self.message.chat.id, self.text, parse_mode="MarkdownV2")
    
    def get_user(self):
        sql = """select * from users where user_id = :user_id"""
        user = db.fetch_one(sql, {"user_id": self.message.from_user.id})
        self.user = user
        self.get_verb()
    
    def get_clear_word(self):
        verb = random.choice(self.verbs)

        if "-" in verb.first_form:
            return self.get_clear_word()
        
        return verb

    def get_verb(self):
        verb = self.get_clear_word()
        self.text += "Example of answer `Second form, Third form`\n"
        self.text += f"The first form of verb is {verb.first_form}\."
        self.set_last_verb(verb.first_form)
    
    def set_last_verb(self, verb_id):
        sql = "UPDATE users SET verb_id = :verb_id WHERE user_id = :user_id"
        params = {"verb_id": verb_id, "user_id": self.message.from_user.id}
        db.execute(sql, params)

    def check_user_answer(self):
        splited_text = self.message.text.split(",")
        res = None
        try:
            for obj in self.verbs:
                if obj.second_form == splited_text[0].lower().strip() and obj.third_form == splited_text[1].lower().strip():
                    res = True

            if res:
                self.right_answer()
            else:
                self.wrong_answer()

        except IndexError as e:
            self.text += "I can\`t understand you\. Be shure to use right format of answer\."
    
    def right_answer(self):
        self.text += "You are right\!\n"
        self.get_user()
    
    def wrong_answer(self):
        self.text += "Incorrectly\.\n"
        self.text += "Please\, try again or switch to self\-input state and check the forms\."