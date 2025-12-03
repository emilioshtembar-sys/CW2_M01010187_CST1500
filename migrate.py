import pandas as pd 
from app.users import add_user, add_incident, add_ticket, add_dataset



def migrate_users(conn):
    with open('DATA\\users.py', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
    add_user(conn, name, hash)
    print(user.strip()) 
    conn.close()



def migrate_tickets(conn):
    with open('DATA\\ITtickets.py', 'r') as f:
        tickets = f.readlines()
    for t in tickets:
        title, desc, status = t.strip().split(',')
        add_ticket(conn, title, desc, status)
        print(f"Added ticket: {title}")

def migrate_datasets(conn):
    with open('DATA\\datasets.py', 'r') as f:
        datasets = f.readlines()
    for ds in datasets:
        name, desc = ds.strip().split(',')
    add_dataset(conn, name, desc)
    print(f"Added dataset: {name}")
    conn.close()

def migrate_incidents(conn):
    with open('DATA\\incidents.py', 'r') as f:
        incidents = f.readlines()
    for inc in incidents:
        title, description, severity, status, reporter = inc.strip().split(',')
    add_incident(conn, title, description, severity, status, reporter)
    print(inc.strip())
    conn.close()


