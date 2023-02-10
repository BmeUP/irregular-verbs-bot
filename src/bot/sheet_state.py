from .state_interface import IState

class SheetState(IState):
    def __init__(self, message, bot) -> None:
        self.message = message
        self.bot = bot

    def process_message(self):
        with open("src/list-of-irregular-verbs.pdf", "rb") as f:
            _file = f.read()
        
        self.bot.send_document(
            self.message.chat.id, 
            document=_file, visible_file_name="list-of-irregular-verbs.pdf")