import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Datasets CRUD", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DATA')
DB_PATH = os.path.join(DATA_DIR, 'Datsets&Metadata_platform.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_dataset(name, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO datasets (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()

def read_datasets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, description, created_at FROM datasets')
    datasets = cur.fetchall()
    conn.close()
    return datasets

def update_dataset(dataset_id, name, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE datasets SET name = ?, description = ? WHERE id = ?', (name, description, dataset_id))
    conn.commit()
    conn.close()

def delete_dataset(dataset_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM datasets WHERE id = ?', (dataset_id,))
    conn.commit()
    conn.close()

st.title("📂 Datasets CRUD")

tab1, tab2, tab3, tab4 = st.tabs(["Read", "Create", "Update", "Delete"])

# READ
with tab1:
    st.subheader("View All Datasets")
    datasets = read_datasets()
    if datasets:
        for dataset in datasets:
            st.write(f"**ID:** {dataset['id']} | **Name:** {dataset['name']}")
            st.write(f"Description: {dataset['description']}")
            st.write(f"Created: {dataset['created_at']}")
            st.divider()
    else:
        st.info("No datasets found.")

# CREATE
with tab2:
    st.subheader("Add New Dataset")
    new_name = st.text_input("Dataset Name")
    new_desc = st.text_area("Description")
    if st.button("Create Dataset"):
        if new_name and new_desc:
            create_dataset(new_name, new_desc)
            st.success("Dataset created successfully!")
        else:
            st.error("Please fill in all fields.")

# UPDATE
with tab3:
    st.subheader("Update Dataset")
    datasets = read_datasets()
    if datasets:
        dataset_id = st.selectbox("Select Dataset ID", [d['id'] for d in datasets])
        selected_dataset = next(d for d in datasets if d['id'] == dataset_id)
        updated_name = st.text_input("Name", value=selected_dataset['name'])
        updated_desc = st.text_area("Description", value=selected_dataset['description'])
        if st.button("Update Dataset"):
            update_dataset(dataset_id, updated_name, updated_desc)
            st.success("Dataset updated successfully!")
    else:
        st.info("No datasets to update.")

# DELETE
with tab4:
    st.subheader("Delete Dataset")
    datasets = read_datasets()
    if datasets:
        dataset_id = st.selectbox("Select Dataset ID to Delete", [d['id'] for d in datasets], key="delete_dataset")
        if st.button("Delete Dataset", key="delete_btn_dataset"):
            delete_dataset(dataset_id)
            st.success("Dataset deleted successfully!")
    else:
        st.info("No datasets to delete.")
