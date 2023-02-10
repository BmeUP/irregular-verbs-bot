from .db import db

class CheckUser():
    def __call__(self, fn):
        def wraper(*args, **kwargs):
            self.message = args[0]
            self.check_user()
            fn(*args, **kwargs)
        return wraper
    
    def check_user(self):
        sql = """select * from users where user_id = :user_id"""
        user = db.fetch_one(sql, {"user_id": self.message.from_user.id})
        
        if user is None:
            self.create_user()
    
    def create_user(self):
        sql = """insert into users(user_id, state) values(:user_id, 'selfinput')"""
        db.execute(sql, {"user_id": self.message.from_user.id})
