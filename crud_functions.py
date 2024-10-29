import sqlite3
from pprint import pprint

def initiate_db():
    SQL = '''
    CREATE TABLE IF NOT EXISTS Vines (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER,
    pic_fn TEXT);
    '''
    connection = sqlite3.connect('TG_bot_II.db')
    cursor = connection.cursor()
    cursor.execute(SQL)
    connection.commit()
    SQL = '''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL);
        '''
    cursor.execute(SQL)
    connection.commit()
    connection.close()

def is_user(username):
    SQL = f'SELECT * FROM Users WHERE username="{username}"'
    connection = sqlite3.connect('TG_bot_II.db')
    cursor = connection.cursor()
    cursor.execute(SQL)
    user = cursor.fetchall()
    if len(user) == 0:
        result = False
    else:
        result = True
    connection.commit()
    connection.close()
    return result

def add_user(username, email, age):
    if not is_user(username):
        SQL = f'INSERT INTO USERS(username, email, age, balance) VALUES ("{username}", "{email}", {age}, 10000);'
        print(SQL)
        connection = sqlite3.connect('TG_bot_II.db')
        cursor = connection.cursor()
        cursor.execute(SQL)
        connection.commit()
        connection.close()
        return True
    else:
        return False
def get_all_products():
    SQL = 'SELECT * FROM Vines'
    connection = sqlite3.connect('TG_bot_II.db')
    cursor = connection.cursor()
    cursor.execute(SQL)
    vines = cursor.fetchall()
    # for i in vines:
    #     pprint(i)
    connection.commit()
    connection.close()
    return vines
