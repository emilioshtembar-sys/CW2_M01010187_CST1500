import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Cyber Incidents CRUD", layout="wide")

# Using cyberintelligence_platform.db for cybersecurity incidents
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DATA')
DB_PATH = os.path.join(DATA_DIR, 'cyberintelligence_platform.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create cyber_incidents table if it doesn't exist"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def create_incident(incident_type, severity, description, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''INSERT INTO cyber_incidents (incident_type, severity, description, status) 
                   VALUES (?, ?, ?, ?)''', (incident_type, severity, description, status))
    conn.commit()
    conn.close()

def read_incidents():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, incident_type, severity, description, status, created_at FROM cyber_incidents')
    incidents = cur.fetchall()
    conn.close()
    return incidents

def update_incident(incident_id, incident_type, severity, description, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''UPDATE cyber_incidents SET incident_type = ?, severity = ?, description = ?, status = ? 
                   WHERE id = ?''', (incident_type, severity, description, status, incident_id))
    conn.commit()
    conn.close()

def delete_incident(incident_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM cyber_incidents WHERE id = ?', (incident_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

st.title("🛡️ Cybersecurity Incidents CRUD")

tab1, tab2, tab3, tab4 = st.tabs(["Read", "Create", "Update", "Delete"])

# READ
with tab1:
    st.subheader("View All Incidents")
    incidents = read_incidents()
    if incidents:
        for incident in incidents:
            severity_color = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
            color = severity_color.get(incident['severity'], "⚪")
            st.write(f"{color} **ID:** {incident['id']} | **Type:** {incident['incident_type']} | **Severity:** {incident['severity']}")
            st.write(f"Description: {incident['description']}")
            st.write(f"Status: {incident['status']} | Created: {incident['created_at']}")
            st.divider()
    else:
        st.info("No incidents found.")

# CREATE
with tab2:
    st.subheader("Report New Incident")
    new_type = st.text_input("Incident Type (e.g., Phishing, Malware, DDoS)")
    new_severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
    new_desc = st.text_area("Description")
    new_status = st.selectbox("Status", ["open", "investigating", "contained", "resolved"])
    if st.button("Create Incident"):
        if new_type and new_desc:
            create_incident(new_type, new_severity, new_desc, new_status)
            st.success("Incident reported successfully!")
        else:
            st.error("Please fill in all fields.")

# UPDATE
with tab3:
    st.subheader("Update Incident")
    incidents = read_incidents()
    if incidents:
        incident_id = st.selectbox("Select Incident ID", [i['id'] for i in incidents])
        selected_incident = next(i for i in incidents if i['id'] == incident_id)
        updated_type = st.text_input("Incident Type", value=selected_incident['incident_type'])
        updated_severity = st.selectbox("Severity", ["low", "medium", "high", "critical"],
                                       index=["low", "medium", "high", "critical"].index(selected_incident['severity']))
        updated_desc = st.text_area("Description", value=selected_incident['description'])
        updated_status = st.selectbox("Status", ["open", "investigating", "contained", "resolved"],
                                     index=["open", "investigating", "contained", "resolved"].index(selected_incident['status']))
        if st.button("Update Incident"):
            update_incident(incident_id, updated_type, updated_severity, updated_desc, updated_status)
            st.success("Incident updated successfully!")
    else:
        st.info("No incidents to update.")

# DELETE
with tab4:
    st.subheader("Delete Incident")
    incidents = read_incidents()
    if incidents:
        incident_id = st.selectbox("Select Incident ID to Delete", [i['id'] for i in incidents], key="delete_incident")
        if st.button("Delete Incident", key="delete_btn_incident"):
            delete_incident(incident_id)
            st.success("Incident deleted successfully!")
    else:
        st.info("No incidents to delete.")
