import pandas as pd
from app.users import add_user, add_ticket, add_dataset

def add_ticket(conn, user_id, issue, status="open"):
    curr = conn.cursor()
    sql = '''INSERT INTO tickets (user_id, issue, status)
             VALUES (?, ?, ?)'''
    param = (user_id, issue, status)
    curr.execute(sql, param)
    conn.commit()


def get_ticket_by_id(conn, ticket_id):
    curr = conn.cursor()
    sql = '''SELECT * FROM tickets WHERE id = ?'''
    param = (ticket_id,)
    curr.execute(sql, param)
    ticket = curr.fetchone()
    conn.close()
    return ticket

def delete_ticket(conn, ticket_id):
    curr = conn.cursor()
    sql = '''DELETE FROM tickets WHERE id = ?'''
    param = (ticket_id,)
    curr.execute(sql, param)

def get_all_tickets_pandas(conn):
    query = "SELECT * FROM tickets"
    df = pd.read_sql_query(query, conn)
    return df


def update_ticket_status(conn, ticket_id, new_status):
    curr = conn.cursor()
    sql = '''UPDATE tickets SET status = ? WHERE id = ?'''
    param = (new_status, ticket_id)
    curr.execute(sql, param)
    conn.commit()