import sqlite3

import fitz

def main():
    reader = fitz.open("list-of-irregular-verbs.pdf")
    for page in reader:  # iterate the document pages
        text = page.get_text()  # get plain text (is in UTF-8)
        get_three_words(text.split("\n")[8:])
        

def get_three_words(string):
    f_index = 0
    s_index = 3
    for _ in range(0, len(string) + 1):
        data = string[f_index:s_index]
        if len(data):
            print("============")
            print(data)
            print("============")
            try:
                to_db([data[0], data[1], data[2]])
            except Exception:
                pass
        f_index = s_index
        s_index += 3

def to_db(data):
    con = sqlite3.connect("iverbs.db")
    cur = con.cursor()
    __sql__ = """insert into iverbs(first_form, second_form, third_form) values(?, ?, ?)"""
    cur.execute(__sql__, data)
    con.commit()
    con.close()

main()