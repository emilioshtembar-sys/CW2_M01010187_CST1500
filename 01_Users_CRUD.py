import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Users CRUD", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DATA')
DB_PATH = os.path.join(DATA_DIR, 'users_platform.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(username, password_hash):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def read_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, username, password_hash FROM users')
    users = cur.fetchall()
    conn.close()
    return users

def update_user(user_id, username, password_hash):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE users SET username = ?, password_hash = ? WHERE id = ?', (username, password_hash, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

st.title("👥 Users CRUD")

tab1, tab2, tab3, tab4 = st.tabs(["Read", "Create", "Update", "Delete"])

# READ
with tab1:
    st.subheader("View All Users")
    users = read_users()
    if users:
        for user in users:
            st.write(f"**ID:** {user['id']} | **Username:** {user['username']} | **Hash:** {user['password_hash'][:20]}...")
    else:
        st.info("No users found.")

# CREATE
with tab2:
    st.subheader("Add New User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password Hash", type="password")
    if st.button("Create User"):
        if new_username and new_password:
            if create_user(new_username, new_password):
                st.success(f"User '{new_username}' created successfully!")
            else:
                st.error("Username already exists.")
        else:
            st.error("Please fill in all fields.")

# UPDATE
with tab3:
    st.subheader("Update User")
    users = read_users()
    if users:
        user_id = st.selectbox("Select User ID", [u['id'] for u in users])
        selected_user = next(u for u in users if u['id'] == user_id)
        updated_username = st.text_input("New Username", value=selected_user['username'])
        updated_password = st.text_input("New Password Hash", value=selected_user['password_hash'], type="password")
        if st.button("Update User"):
            update_user(user_id, updated_username, updated_password)
            st.success("User updated successfully!")
    else:
        st.info("No users to update.")

# DELETE
with tab4:
    st.subheader("Delete User")
    users = read_users()
    if users:
        user_id = st.selectbox("Select User ID to Delete", [u['id'] for u in users], key="delete_user")
        if st.button("Delete User", key="delete_btn_user"):
            delete_user(user_id)
            st.success("User deleted successfully!")
    else:
        st.info("No users to delete.")
