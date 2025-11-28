import pandas as pd
from app.users import add_user, add_ticket, add_dataset 
def add_incident(conn, title, description, severity, date_reported):
    curr = conn.cursor()
    sql = '''INSERT INTO incidents (title, description, severity, date_reported)
             VALUES (?, ?, ?, ?)'''
    param = (title, description, severity, date_reported)
    curr.execute(sql, param)
    conn.commit()

def get_all_incidents(conn):
    curr = conn.cursor()
    sql = '''SELECT * FROM incidents'''
    curr.execute(sql)
    incidents = curr.fetchall()
    conn.close()
    return incidents

def get_incident_by_id(conn, incident_id):
    curr = conn.cursor()
    sql = '''SELECT * FROM incidents WHERE id = ?'''
    param = (incident_id,)
    curr.execute(sql, param)
    incident = curr.fetchone()
    conn.close()
    return incident

def delete_incident(conn, incident_id):
    curr = conn.cursor()
    sql = '''DELETE FROM incidents WHERE id = ?'''
    param = (incident_id,)
    curr.execute(sql, param)
    conn.commit()

def get_all_incidents_pandas(conn):
    query = "SELECT * FROM incidents"
    df = pd.read_sql_query(query, conn)
    return df


def update_incident_severity(conn, incident_id, new_severity):
    curr = conn.cursor()
    sql = '''UPDATE incidents SET severity = ? WHERE id = ?'''
    param = (new_severity, incident_id)
    curr.execute(sql, param)
    conn.commit()