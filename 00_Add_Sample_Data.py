import streamlit as st
import sqlite3
import os

st.set_page_config(page_title="Add Sample Data", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DATA')

def add_sample_data():
    """Add all sample data to databases"""
    
    # ============ ADD USERS ============
    users_db = os.path.join(DATA_DIR, 'users_platform.db')
    conn = sqlite3.connect(users_db)
    cur = conn.cursor()
    
    users = [
        ('admin', 'hashed_password_123'),
        ('john_doe', 'hashed_password_456'),
        ('jane_smith', 'hashed_password_789'),
        ('security_team', 'hashed_password_101'),
        ('analyst', 'hashed_password_202'),
    ]
    
    users_added = 0
    for username, password_hash in users:
        try:
            cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                       (username, password_hash))
            users_added += 1
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    
    # ============ ADD TICKETS ============
    tickets_db = os.path.join(DATA_DIR, 'ITtickets_platform.db')
    conn = sqlite3.connect(tickets_db)
    cur = conn.cursor()
    
    tickets = [
        ('Email not working', 'User cannot access email on laptop', 'open'),
        ('Printer offline', 'Printer in building B is offline', 'in_progress'),
        ('Password reset', 'Forgot password for VPN access', 'closed'),
        ('Software installation', 'Need Python 3.11 installed on workstation', 'open'),
        ('Network latency', 'Slow internet connection affecting downloads', 'in_progress'),
    ]
    
    tickets_added = 0
    for title, desc, status in tickets:
        try:
            cur.execute('INSERT INTO tickets (title, description, status) VALUES (?, ?, ?)',
                       (title, desc, status))
            tickets_added += 1
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    
    # ============ ADD INCIDENTS ============
    cyber_db = os.path.join(DATA_DIR, 'cyberintelligence_platform.db')
    conn = sqlite3.connect(cyber_db)
    cur = conn.cursor()
    
    incidents = [
        ('Phishing', 'high', 'Suspicious email with malware attachment detected', 'investigating'),
        ('Malware', 'critical', 'Ransomware detected on 3 workstations', 'contained'),
        ('DDoS', 'medium', 'Website under DDoS attack from unknown source', 'mitigated'),
        ('Data exfiltration', 'critical', 'Unauthorized file transfer detected', 'investigating'),
        ('Account compromise', 'high', 'Admin account accessed from unknown location', 'contained'),
    ]
    
    incidents_added = 0
    for incident_type, severity, description, status in incidents:
        try:
            cur.execute('''INSERT INTO cyber_incidents (incident_type, severity, description, status) 
                          VALUES (?, ?, ?, ?)''',
                       (incident_type, severity, description, status))
            incidents_added += 1
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    
    # ============ ADD DATASETS ============
    datasets_db = os.path.join(DATA_DIR, 'Datsets&Metadata_platform.db')
    conn = sqlite3.connect(datasets_db)
    cur = conn.cursor()
    
    datasets = [
        ('User Activity Logs', 'Daily logs of user authentication and system access'),
        ('Sales Data 2024', 'Monthly sales figures across all regions for fiscal year 2024'),
        ('Network Traffic', 'Real-time network traffic data for anomaly detection'),
        ('Customer Feedback', 'Survey responses and feedback from customer satisfaction studies'),
        ('Financial Records', 'Quarterly financial reports and balance sheets'),
    ]
    
    datasets_added = 0
    for name, description in datasets:
        try:
            cur.execute('INSERT INTO datasets (name, description) VALUES (?, ?)',
                       (name, description))
            datasets_added += 1
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    
    return {
        'users': users_added,
        'tickets': tickets_added,
        'incidents': incidents_added,
        'datasets': datasets_added
    }

st.title("📥 Add Sample Data")

st.write("""
Click the button below to populate your databases with sample data:
- **5 Users** (admin, analysts, security team)
- **5 IT Tickets** (various statuses)
- **5 Cybersecurity Incidents** (various severities)
- **5 Datasets** (sample datasets with descriptions)
""")

if st.button("Add Sample Data Now", key="add_data_btn", help="Click to populate databases"):
    try:
        results = add_sample_data()
        st.success("✅ Sample data added successfully!")
        st.write(f"""
        **Data Added:**
        - Users: {results['users']}
        - Tickets: {results['tickets']}
        - Incidents: {results['incidents']}
        - Datasets: {results['datasets']}
        """)
        st.info("Go to the CRUD pages in the sidebar to view, edit, and manage this data!")
    except Exception as e:
        st.error(f"❌ Error adding data: {str(e)}")

st.divider()
st.write("**Note:** If data already exists, duplicates will be skipped. You can safely click this button multiple times.")
