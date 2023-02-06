import sqlite3


def main():
    con = sqlite3.connect("iverbs.db")
    cur = con.cursor()
    create_table_iverbs(cur)
    create_table_users(cur)


def create_table_iverbs(cur):
    __sql__ = """CREATE TABLE IF NOT EXISTS iverbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_form TEXT,
                second_form TEXT,
                third_form TEXT
                );"""
    
    cur.execute(__sql__)

def create_table_users(cur):
    __sql__ = """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                state TEXT
                );"""

main()