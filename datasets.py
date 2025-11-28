import pandas as pd
from app.users import add_user, add_ticket, add_dataset
def add_dataset(conn, name, metadata):
    curr = conn.cursor()
    sql = '''INSERT INTO datasets (name, metadata)
             VALUES (?, ?)'''
    param = (name, metadata)
    curr.execute(sql, param)
    conn.commit()


def get_dataset_by_id(conn, dataset_id):
    curr = conn.cursor()
    sql = '''SELECT * FROM datasets WHERE id = ?'''
    param = (dataset_id,)
    curr.execute(sql, param)
    dataset = curr.fetchone()
    conn.close()
    return dataset


def get_all_datasets(conn):
    curr = conn.cursor()
    sql = '''SELECT * FROM datasets'''
    curr.execute(sql)
    datasets = curr.fetchall()
    conn.close()
    return datasets

def delete_dataset(conn, dataset_id):
    curr = conn.cursor()
    sql = '''DELETE FROM datasets WHERE id = ?'''
    param = (dataset_id,)
    curr.execute(sql, param)
    conn.commit()


def update_dataset_metadata(conn, dataset_id, new_metadata):
    curr = conn.cursor()
    sql = '''UPDATE datasets SET metadata = ? WHERE id = ?'''
    param = (new_metadata, dataset_id)
    curr.execute(sql, param)
    conn.commit()

def get_all_datasets_pandas(conn):
    query = "SELECT * FROM datasets"
    df = pd.read_sql_query(query, conn)
    return df