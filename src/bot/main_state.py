from .db import db
from .self_input_state import SelfInputState


class State():
    def __init__(self) -> None:
        self.states = {}
    
    def register_new_state(self, name, state_obj):
        self.states.update({
            name: state_obj
        })
    
    def choose(self, message, bot):
        self.current_state = self.states.get(self.check_user_state(message))(message, bot)
        self.current_state.process_message()
    
    def check_user_state(self, message):
        sql = """select * from users where user_id = :user_id;"""
        params = {"user_id": message.from_user.id}
        user = db.fetch_one(sql, params)
        return user[2]

states = State()
states.register_new_state("self-input", SelfInputState)