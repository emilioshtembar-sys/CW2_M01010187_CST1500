import streamlit as st
import sqlite3
import os
from datetime import datetime

st.set_page_config(page_title="IT Tickets CRUD", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DATA')
DB_PATH = os.path.join(DATA_DIR, 'ITtickets_platform.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_ticket(title, description, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO tickets (title, description, status) VALUES (?, ?, ?)', 
                (title, description, status))
    conn.commit()
    conn.close()

def read_tickets():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, title, description, status, created_at FROM tickets')
    tickets = cur.fetchall()
    conn.close()
    return tickets

def update_ticket(ticket_id, title, description, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE tickets SET title = ?, description = ?, status = ? WHERE id = ?',
                (title, description, status, ticket_id))
    conn.commit()
    conn.close()

def delete_ticket(ticket_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))
    conn.commit()
    conn.close()

st.title("🎫 IT Tickets CRUD")

tab1, tab2, tab3, tab4 = st.tabs(["Read", "Create", "Update", "Delete"])

# READ
with tab1:
    st.subheader("View All Tickets")
    tickets = read_tickets()
    if tickets:
        for ticket in tickets:
            st.write(f"**ID:** {ticket['id']} | **Title:** {ticket['title']} | **Status:** {ticket['status']}")
            st.write(f"Description: {ticket['description']}")
            st.write(f"Created: {ticket['created_at']}")
            st.divider()
    else:
        st.info("No tickets found.")

# CREATE
with tab2:
    st.subheader("Create New Ticket")
    new_title = st.text_input("Ticket Title")
    new_desc = st.text_area("Description")
    new_status = st.selectbox("Status", ["open", "in_progress", "closed"])
    if st.button("Create Ticket"):
        if new_title and new_desc:
            create_ticket(new_title, new_desc, new_status)
            st.success("Ticket created successfully!")
        else:
            st.error("Please fill in all fields.")

# UPDATE
with tab3:
    st.subheader("Update Ticket")
    tickets = read_tickets()
    if tickets:
        ticket_id = st.selectbox("Select Ticket ID", [t['id'] for t in tickets])
        selected_ticket = next(t for t in tickets if t['id'] == ticket_id)
        updated_title = st.text_input("Title", value=selected_ticket['title'])
        updated_desc = st.text_area("Description", value=selected_ticket['description'])
        updated_status = st.selectbox("Status", ["open", "in_progress", "closed"], 
                                     index=["open", "in_progress", "closed"].index(selected_ticket['status']))
        if st.button("Update Ticket"):
            update_ticket(ticket_id, updated_title, updated_desc, updated_status)
            st.success("Ticket updated successfully!")
    else:
        st.info("No tickets to update.")

# DELETE
with tab4:
    st.subheader("Delete Ticket")
    tickets = read_tickets()
    if tickets:
        ticket_id = st.selectbox("Select Ticket ID to Delete", [t['id'] for t in tickets], key="delete_ticket")
        if st.button("Delete Ticket", key="delete_btn_ticket"):
            delete_ticket(ticket_id)
            st.success("Ticket deleted successfully!")
    else:
        st.info("No tickets to delete.")
