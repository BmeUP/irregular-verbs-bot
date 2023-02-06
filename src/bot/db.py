import sqlite3


class Db():
    def __init__(self) -> None:
        self.con = sqlite3.connect("iverbs.db", check_same_thread=False)
        self.cur = self.con.cursor()
    
    def fetch_one(self, sql, params):
        self.cur.execute(sql, params)
        res = self.cur.fetchone()
        return res

    def execute(self, sql, params):
        self.cur.execute(sql, params)
        self.con.commit()

db = Db()