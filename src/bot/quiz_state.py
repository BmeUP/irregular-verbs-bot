from .state_interface import IState
from .db import db

class QuizState(IState):
    def __init__(self, message, bot) -> None:
        self.message = message
        self.bot = bot
        self.text = ""
        self.user = None
    
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
    
    def get_verb(self):
        sql = """SELECT i.id, i.first_form FROM iverbs i 
                 WHERE id != :id ORDER BY RANDOM() LIMIT 1;"""
        params = {"id": 0 if self.user[3] is None else self.user[3]}
        verb = db.fetch_one(sql, params)
        self.text += "Example of answer `Second form, Third form`\n"
        self.text += f"The first form of verb is {verb[1]}\."
        self.set_last_verb(verb[0])
    
    def set_last_verb(self, verb_id):
        sql = "UPDATE users SET verb_id = :verb_id"
        params = {"verb_id": verb_id}
        db.execute(sql, params)

    def check_user_answer(self):
        splited_text = self.message.text.split(",")

        try:
            second_form = splited_text[0].strip().lower()
            third_form = splited_text[1].strip().lower()
            sql = """SELECT id FROM iverbs 
                     where (second_form = :second_form and 
                            third_form = :third_form);"""
            params = {"second_form": f"{second_form} ", "third_form": f"{third_form} "}
            res = db.fetch_one(sql, params)
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