import pandas as pd
from app.users import add_user, add_ticket, add_dataset
def add_user(conn, name, hash): 
    curr = conn.cursor()
    sql = ('''INSERT INTO users (username, password_hash) VALUES (?, ?)''')
    param = (name, hash)
    curr.execute(sql, param)
    conn.commit()

def get_user_by_name(conn, name):
    curr = conn.cursor()
    sql = ('''SELECT * FROM users WHERE username = ?''')
    param = (name,)
    curr.execute(sql, param)
    user = curr.fetchone()
    conn.close()
    return user


def get_all_users(conn):
    curr = conn.cursor()
    sql = ('''SELECT * FROM users''')
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return users 

def delete_user(conn, username):
    curr = conn.cursor()
    sql = '''DELETE FROM users WHERE username = ?'''
    param = (username,)
    curr.execute(sql, param)
    conn.commit()

def get_all_users_pandas(conn):
    query = "SELECT * FROM users"
    df = pd.read_sql_query(query, conn)
    return df


def update_user_password(conn, username, new_hash):
    curr = conn.cursor()
    sql = '''UPDATE users SET password_hash = ? WHERE username = ?'''
    param = (new_hash, username)
    curr.execute(sql, param)
    conn.commit()