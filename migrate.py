import pandas as pd 
from app.users import add_user,



def migrate_users(conn):
    with open('DATA\\user.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
    add_user(conn, name, hash)
    print(user.strip()) 
    conn.close()



def migrate_tickets(conn, filepath='DATA\\ITtickets.txt'):
    with open(filepath, 'r') as f:
        tickets = f.readlines()
    for t in tickets:
        title, desc, status = t.strip().split(',')
        add_ticket(conn, title, desc, status)
        print(f"Added ticket: {title}")

def migrate_datasets(conn, filepath='DATA\\datasets.txt'):
    with open(filepath, 'r') as f:
        datasets = f.readlines()
    for ds in datasets:
        name, desc = ds.strip().split(',')
        add_dataset(conn, name, desc)
        print(f"Added dataset: {name}")