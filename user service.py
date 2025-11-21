import pandas as pd
from app.users import add_user, add_ticket, add_dataset, add_incident  # ensure add_incident is available here

def migrate_users(conn, filepath='DATA\\users.txt'):
    """Import users from file into the database."""
    with open(filepath, 'r') as f:
        users = f.readlines()

    for user in users:
        name, hash_val = user.strip().split(',')
        add_user(conn, name, hash_val)
        print(f"Added user: {name}")

    conn.commit()

def migrate_tickets(conn, filepath='DATA\\ITtickets.txt'):
    """Import tickets from file into the database."""
    with open(filepath, 'r') as f:
        tickets = f.readlines()

    for t in tickets:
        title, desc, status = t.strip().split(',')
        add_ticket(conn, title, desc, status)
        print(f"Added ticket: {title}")

    conn.commit()

def migrate_datasets(conn, filepath='DATA\\datasets.txt'):
    """Import datasets from file into the database."""
    with open(filepath, 'r') as f:
        datasets = f.readlines()

    for ds in datasets:
        name, desc = ds.strip().split(',')
        add_dataset(conn, name, desc)
        print(f"Added dataset: {name}")

    conn.commit()

def migrate_incidents(conn, filepath='DATA\\incidents.txt'):
    """Import incidents from file into the database."""
    with open(filepath, 'r') as f:
        incidents = f.readlines()

    for incident in incidents:
        title, desc, severity = incident.strip().split(',')
        add_incident(conn, title, desc, severity)
        print(f"Added incident: {title}")

    conn.commit()