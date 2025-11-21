import sqlite3


# Cyber intelligence
conn = sqlite3.connect('DATA\\intelligence_platform.db') 
curr =conn.cursor()
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




# Datasets and metadata
conn = sqlite3.connect('DATA\\intelligence_platform.db')
curr = conn.cursor()

sql_datasets = '''CREATE TABLE IF NOT EXISTS datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

curr.execute(sql_datasets)
conn.commit()
conn.close()






# Users table
conn = sqlite3.connect('DATA\\intelligence_platform.db')
curr = conn.cursor()
sql_users = '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

curr.execute(sql_users)
conn.commit()
conn.close()





# Tickets table 
conn = sqlite3.connect('DATA\\ITtickets_platform.db') 
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


