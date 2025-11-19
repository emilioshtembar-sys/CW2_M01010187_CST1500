import sqlite3


conn = sqlite3.connect('DATA/cyberintelligence_platform.db') 

def add_user(conn, username, hashed_password):
    curr = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    curr.execute(sql, (username, hashed_password))
    conn.commit()
    param = (username, hash)
    curr.execute(sql, param)
    conn.commit()

    

def get_users(): 
    

    curr = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return users 


def migrate_users():
    with open('DATA/user.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
    add_user(conn, name, hash)
    print(user.strip()) 








def add_dataset(conn, name, description=None):
    curr = conn.cursor()
    sql = '''INSERT INTO datasets (name, description) VALUES (?, ?)'''
    curr.execute(sql, (name, description))
    conn.commit()

def get_dataset(conn, name):
    curr = conn.cursor()
    sql = '''SELECT * FROM datasets WHERE name = ?'''
    curr.execute(sql, (name,))
    return curr.fetchall()

def migrate_datasets(conn, filepath='DATA/datasets.txt'):
    with open(filepath, 'r') as f:
        datasets = f.readlines()
    for ds in datasets:
        name, desc = ds.strip().split(',')
        add_dataset(conn, name, desc)
        print(f"Added dataset: {name}")







def add_user(conn, username, hashed_password):
    curr = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    curr.execute(sql, (username, hashed_password))
    conn.commit()

def get_user(conn, username):
    curr = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    curr.execute(sql, (username,))
    return curr.fetchall()

def migrate_users(conn, filepath='DATA/user.txt'):
    with open(filepath, 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash_val = user.strip().split(',')
        add_user(conn, name, hash_val)
        print(f"Added: {name}")








conn = sqlite3.connect('DATA/ITtickets_platform.db') 
curr =conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''
curr.execute(sql)
conn.commit()
conn.close()



def add_ticket(conn, title, description, status='open'):
    curr = conn.cursor()
    sql = '''INSERT INTO tickets (title, description, status) VALUES (?, ?, ?)'''
    curr.execute(sql, (title, description, status))
    conn.commit()

def get_ticket(conn, ticket_id):
    curr = conn.cursor()
    sql = '''SELECT * FROM tickets WHERE id = ?'''
    curr.execute(sql, (ticket_id,))
    return curr.fetchone()

def migrate_tickets(conn, filepath='DATA/ITtickets.txt'):
    with open(filepath, 'r') as f:
        tickets = f.readlines()
    for t in tickets:
        title, desc, status = t.strip().split(',')
        add_ticket(conn, title, desc, status)
        print(f"Added ticket: {title}")
