import json

from .db import db
from .self_input_state import SelfInputState
from .quiz_state import QuizState
from .sheet_state import SheetState
from .dict_model import DictModel


class State():
    def __init__(self) -> None:
        self.states = {}
        self.verbs = []
    
    def register_new_state(self, name, state_obj):
        self.states.update({
            name: state_obj
        })
    
    def choose(self, message, bot):
        self.bot = bot
        self.current_state = self.states.get(self.check_user_state(message))(message, self.bot, self.verbs)
        self.current_state.process_message()
    
    def check_user_state(self, message):
        sql = """select * from users where user_id = :user_id;"""
        params = {"user_id": message.from_user.id}
        user = db.fetch_one(sql, params)

        if user[2] != message.text and message.text in ["SelfInput", "Quiz"]:
            self.update_user_state(message)
            return message.text
        elif message.text == "Gimme that sheet!":
            return "GTS"

        return user[2]

    def update_user_state(self, message):
        sql = """update users set state = :state where user_id = :user_id;"""
        params = {"state": message.text, "user_id": message.from_user.id}
        db.execute(sql, params)
        self.text = f"Now we are in {message.text} state\."
        self.bot.send_message(message.chat.id, self.text, parse_mode="MarkdownV2")

    def get_verbs(self):
        with open("src/bot/irregular_verbs.json") as json_file:
            dct_verbs = json.load(json_file)

            for key in dct_verbs:
                obj = dct_verbs.get(key)[0]
                self.verbs.append(
                    DictModel(
                        first_form=key,
                        second_form=obj.get("2")[0],
                        third_form=obj.get("3")[0],
                        description=obj.get("description")
                    )
                )

states = State()
states.get_verbs()
states.register_new_state("SelfInput", SelfInputState)
states.register_new_state("Quiz", QuizState)
# states.register_new_state("GTS", SheetState)