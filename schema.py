import sqlite3


# Cyber intelligence table 
def create_user_table(conn):
    conn = sqlite3.connect("DATA\\cyberintelligence.db")
    curr = conn.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                THREAT_LEVEL TEXT,
    SEVERITY TEXT,
    INCIDENTS_REPORTED INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );'''
    curr.execute(sql)
    conn.commit()
    conn.close()

with sqlite3.connect("DATA\\cyberintelligence.db") as conn:
    create_user_table(conn)
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    param = ("admin", "hashed_password_123")
    conn.execute(sql, param)
    conn.commit()



# Users table
def create_users_table(conn):
    conn = sqlite3.connect('DATA\\intelligence_platform.db')
    curr = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );'''
    curr.execute(sql)
    conn.commit()
    conn.close()

with sqlite3.connect("DATA\\cyberintelligence.db") as conn:
    create_user_table(conn)
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    param = ("admin", "hashed_password_123")
    conn.execute(sql, param)
    conn.commit()



# Datasets and metadata table 
def create_dataset_table(conn):
    conn = sqlite3.connect("DATA\\Datasets&Metadata_platform.db")
    curr = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
    curr.execute(sql)
    conn.commit()
    conn.close()

with sqlite3.connect("DATA\\Datsets&Metadata_platform.db") as conn:
    create_dataset_table(conn)
    sql = '''INSERT INTO datasets (name, description) VALUES (?, ?)'''
    param = ("Threat Intel Feed", "Daily feed of cyber threat indicators")
    conn.execute(sql, param)
    conn.commit()




# Tickets table
def create_ticket_table(conn):
    conn = sqlite3.connect("DATA\\ITtickets_platform.db")
    curr = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );"""
    curr.execute(sql)
    conn.commit()
    conn.close()
with sqlite3.connect("DATA\\ITtickets_platform.db") as conn:
    create_ticket_table(conn)
    sql = '''INSERT INTO tickets (title, description, status) VALUES (?, ?, ?)'''
    param = ("Server Down", "Main server is not responding", "open")
    conn.execute(sql, param)
    conn.commit()
    conn.close()

