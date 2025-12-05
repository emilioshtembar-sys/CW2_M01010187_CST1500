import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os

# Run this file
st.set_page_config(page_title="Domain Dashboards", layout="wide", initial_sidebar_state="expanded")

# ---------------- Session State ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("Navigation")

# Logout button (only when logged in)
if st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Home"
        st.success("You have logged out.")

public_pages = ["Home", "Login"]
protected_pages = ["IT Operations", "Cybersecurity", "Datasets and Metadata"]

pages = public_pages + protected_pages if st.session_state.logged_in else public_pages
page = st.sidebar.radio("Go to:", pages, index=pages.index(st.session_state.page), key="nav_radio")
st.session_state.page = page

# ---------------- Home Page ----------------
if page == "Home":
    st.title("📊 Domain Insight Dashboards")
    st.write("Welcome! Use the sidebar to access dashboards.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=200)

# ---------------- Login Page ----------------
elif page == "Login":
    st.title("🔐 Authentication")
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # ===== LOGIN TAB =====
    with tab1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_btn"):
            try:
                users_db = os.path.join(os.path.dirname(__file__), 'DATA', 'users_platform.db')
                conn = sqlite3.connect(users_db)
                cur = conn.cursor()
                cur.execute('SELECT password_hash FROM users WHERE username = ?', (login_username,))
                result = cur.fetchone()
                conn.close()
                
                if result and result[0] == login_password:
                    st.session_state.logged_in = True
                    st.success("✅ Login successful! Redirecting to IT Operations...")
                    st.session_state.page = "IT Operations"
                else:
                    st.error("❌ Invalid credentials.")
            except Exception as e:
                st.error(f"❌ Login error: {str(e)}")
    
    # ===== REGISTER TAB =====
    with tab2:
        st.subheader("Create New Account")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        
        if st.button("Register", key="register_btn"):
            if not reg_username or not reg_password or not reg_confirm_password:
                st.error("❌ Please fill in all fields.")
            elif len(reg_password) < 6:
                st.error("❌ Password must be at least 6 characters long.")
            elif reg_password != reg_confirm_password:
                st.error("❌ Passwords do not match.")
            else:
                try:
                    users_db = os.path.join(os.path.dirname(__file__), 'DATA', 'users_platform.db')
                    conn = sqlite3.connect(users_db)
                    cur = conn.cursor()
                    # Insert new user (password stored as-is for demo; use hashing in production)
                    cur.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                               (reg_username, reg_password))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"✅ Account created successfully! You can now login with username '{reg_username}'.")
                except sqlite3.IntegrityError:
                    st.error(f"❌ Username '{reg_username}' already exists. Please choose a different username.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ---------------- IT Operations Page ----------------
elif page == "IT Operations":
    if not st.session_state.logged_in:
        st.error("🔒 You must log in to access IT Operations.")
    else:
        # Balloons appear once after login
        if st.session_state.show_balloons:
            st.balloons()
            st.session_state.show_balloons = False

        st.title("🛠️ IT Operations Dashboard")
        st.write("Service desk performance analysis information.")

        rng = np.random.default_rng(11)
        df = pd.DataFrame({
            "assignee": rng.choice(["Alex","Bianca","Chen","Dev"], 50),
            "resolution_hours": rng.integers(1, 72, 50),
            "tickets": rng.integers(1, 20, 50)
        })

        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Tickets", len(df))
        col2.metric("Avg Resolution (hrs)", round(df["resolution_hours"].mean(), 1))
        col3.metric("Max Resolution (hrs)", int(df["resolution_hours"].max()))

        st.divider()

        # Table preview
        st.subheader("Service Desk Records")
        st.dataframe(df, use_container_width=True)

        # Scatter chart
        st.subheader("Tickets vs Resolution Hours")
        st.scatter_chart(df, x="tickets", y="resolution_hours")

        # Bar chart: average resolution by assignee
        avg_resolution = df.groupby("assignee")["resolution_hours"].mean().reset_index()
        st.subheader("Average Resolution Time by Assignee")
        st.bar_chart(avg_resolution, x="assignee", y="resolution_hours")

        st.divider()

        # Governance Recommendations (average-based per assignee)
        st.subheader("Governance Recommendations (Average-based)")
        agg = df.groupby("assignee").agg(
            avg_res_hours=("resolution_hours", "mean"),
            total_tickets=("tickets", "sum")
        ).reset_index()

        recs = []
        for _, r in agg.iterrows():
            # Workload balancing if average resolution is very high
            if r["avg_res_hours"] > 48:
                recs.append((r["assignee"], "Workload balancing", f"Avg resolution {r['avg_res_hours']:.1f} hrs"))
            # Process optimization if workload and average resolution are both high
            if r["total_tickets"] > 60 and r["avg_res_hours"] > 30:
                recs.append((r["assignee"], "Process optimization", f"{int(r['total_tickets'])} tickets, avg {r['avg_res_hours']:.1f} hrs"))
            # Coaching if average is moderately high
            if 36 < r["avg_res_hours"] <= 48:
                recs.append((r["assignee"], "Targeted coaching", f"Avg resolution {r['avg_res_hours']:.1f} hrs"))

        if recs:
            rec_df = pd.DataFrame(recs, columns=["Assignee", "Recommendation", "Rationale"])
            st.dataframe(rec_df, use_container_width=True)
        else:
            st.info("No specific governance recommendations triggered based on current averages.")

        # ===== ADD NEW TICKET =====
        st.divider()
        st.subheader("➕ Add New Service Desk Record")
        with st.form("add_ticket_form"):
            ticket_title = st.text_input("Ticket Title")
            ticket_desc = st.text_area("Description")
            ticket_status = st.selectbox("Status", ["open", "in_progress", "closed"])
            submit_ticket = st.form_submit_button("Add Service Desk Record")
            
            if submit_ticket and ticket_title and ticket_desc:
                try:
                    tickets_db = os.path.join(os.path.dirname(__file__), 'DATA', 'ITtickets_platform.db')
                    conn = sqlite3.connect(tickets_db)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO tickets (title, description, status) VALUES (?, ?, ?)',
                               (ticket_title, ticket_desc, ticket_status))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Ticket '{ticket_title}' created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            elif submit_ticket:
                st.warning("Please fill in all fields.")

# ---------------- Cybersecurity Page ----------------
elif page == "Cybersecurity":
    if not st.session_state.logged_in:
        st.error("🔒 You must log in to access Cybersecurity.")
    else:
        st.title("🛡️ Cybersecurity Dashboard")
        st.write("Phishing spike analysis and response bottlenecks information.")

        rng = np.random.default_rng(42)
        df = pd.DataFrame({
            "category": rng.choice(["Phishing", "Malware", "Ransomware"], 100, p=[0.5, 0.3, 0.2]),
            "resolution_days": rng.integers(1, 15, 100),
            "incidents": rng.integers(1, 10, 100)
        })

        # KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Incidents", len(df))
        col2.metric("Avg Resolution (days)", round(df["resolution_days"].mean(), 1))
        col3.metric("Phishing %", round((df["category"].eq("Phishing").mean())*100, 1))

        st.divider()

        # Table preview
        st.subheader("Incident Records")
        st.dataframe(df, use_container_width=True)

        # Scatter chart
        st.subheader("Incidents vs Resolution Days")
        st.scatter_chart(df, x="incidents", y="resolution_days")

        # Bar chart: average resolution by category
        avg_resolution = df.groupby("category")["resolution_days"].mean().reset_index()
        st.subheader("Average Resolution Time by Category")
        st.bar_chart(avg_resolution, x="category", y="resolution_days")

        st.divider()

        # Governance Recommendations (average-based per category)
        st.subheader("Governance Recommendations (Average-based)")
        agg = df.groupby("category").agg(
            avg_res_days=("resolution_days", "mean"),
            total_incidents=("incidents", "sum")
        ).reset_index()

        recs = []
        for _, r in agg.iterrows():
            cat = r["category"]
            # Enhanced phishing training if phishing averages are high
            if cat == "Phishing" and r["avg_res_days"] > 10:
                recs.append((cat, "Enhanced phishing training", f"Avg resolution {r['avg_res_days']:.1f} days"))
            # Strict containment for ransomware with high incident volume
            if cat == "Ransomware" and r["total_incidents"] > 50:
                recs.append((cat, "Strict containment protocols", f"{int(r['total_incidents'])} ransomware incidents"))
            # Escalation for any category with very high average resolution
            if r["avg_res_days"] > 12:
                recs.append((cat, "Escalation required", f"Avg resolution {r['avg_res_days']:.1f} days"))
            # Playbook optimization for moderate averages
            if 9 < r["avg_res_days"] <= 12:
                recs.append((cat, "Playbook optimization", f"Avg resolution {r['avg_res_days']:.1f} days"))

        if recs:
            rec_df = pd.DataFrame(recs, columns=["Category", "Recommendation", "Rationale"])
            st.dataframe(rec_df, use_container_width=True)
        else:
            st.info("No specific governance recommendations triggered based on current averages.")

        # ===== ADD NEW INCIDENT RECORD =====
        st.divider()
        st.subheader("➕ Add Incident Record")
        with st.form("add_incident_form"):
            incident_type = st.text_input("Incident Type (e.g., Phishing, Malware, DDoS)")
            incident_severity = st.selectbox("Severity", ["low", "medium", "high", "critical"])
            incident_desc = st.text_area("Description")
            incident_status = st.selectbox("Status", ["open", "investigating", "contained", "resolved"])
            submit_incident = st.form_submit_button("Add Incident Record")
            
            if submit_incident:
                if incident_type and incident_desc:  # Check if mandatory fields are filled
                    try:
                        cyber_db = os.path.join(os.path.dirname(__file__), 'DATA', 'cyberintelligence_platform.db')
                        conn = sqlite3.connect(cyber_db)
                        cur = conn.cursor()
                        cur.execute('''INSERT INTO cyber_incidents (incident_type, severity, description, status)
                                       VALUES (?, ?, ?, ?)''',
                                   (incident_type, incident_severity, incident_desc, incident_status))
                        conn.commit()
                        conn.close()
                        st.success(f"✅ Incident '{incident_type}' recorded successfully!")
                    except sqlite3.IntegrityError:
                        st.error("❌ Integrity error: This record cannot be created due to database constraints.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    st.warning("Please fill in all fields.")

# ---------------- Datasets and Metadata Page ----------------
elif page == "Datasets and Metadata":
    if not st.session_state.logged_in:
        st.error("🔒 You must log in to access Datasets and Metadata.")
    else:
        st.title("📂 Datasets and Metadata")
        st.write("Information about datasets used in the dashboards.")
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=200)

        rng = np.random.default_rng(7)
        owners = ["Cyber", "IT", "Analytics", "Finance", "HR"]
        sources = ["S3", "Azure Blob", "On-Prem NAS", "Snowflake", "Google Drive"]

        df = pd.DataFrame({
            "dataset": [f"ds_{i}" for i in range(1, 21)],
            "owner": rng.choice(owners, size=20),
            "source": rng.choice(sources, size=20),
            "size_gb": rng.uniform(1, 200, 20).round(1),
            "rows_millions": rng.uniform(0.1, 100, 20).round(1),
            "dependencies": rng.integers(0, 5, 20),
            "last_accessed": rng.choice(pd.date_range("2025-07-01", "2025-11-30", freq="D"), size=20),
            "pii": rng.choice([True, False], size=20, p=[0.4, 0.6])
        })

        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Datasets", len(df))
        col2.metric("Total size (GB)", round(df["size_gb"].sum(), 1))
        col3.metric("Total rows (M)", round(df["rows_millions"].sum(), 1))
        col4.metric("PII datasets", int(df["pii"].sum()))

        st.divider()

        # Table preview
        st.subheader("Dataset Catalog with Metadata")
        st.dataframe(df, use_container_width=True)

        # Scatter chart
        st.subheader("Dependencies vs Size")
        st.scatter_chart(df, x="dependencies", y="size_gb")

        # Bar chart
        st.subheader("Average Dependencies by Source")
        dep_by_source = df.groupby("source")["dependencies"].mean().reset_index()
        st.bar_chart(dep_by_source, x="source", y="dependencies")

        st.divider()

        # Governance Recommendations
        st.subheader("Governance Recommendations")
        recs = []
        for _, r in df.iterrows():
            days_since_access = (pd.to_datetime("2025-11-30") - r["last_accessed"]).days
            if r["size_gb"] > 100 and r["dependencies"] < 2 and days_since_access > 30:
                recs.append((r["dataset"], "Archive/Cold storage",
                             f"{r['size_gb']} GB, deps={int(r['dependencies'])}, last accessed {r['last_accessed'].date()}"))
            if r["pii"] and r["dependencies"] >= 3:
                recs.append((r["dataset"], "Strict governance (access controls, audits)",
                             f"PII=True, deps={int(r['dependencies'])}"))
            if r["rows_millions"] > 50 and r["source"] in ["S3", "Azure Blob"]:
                recs.append((r["dataset"], "Storage tier optimization",
                             f"Rows={r['rows_millions']}M on {r['source']}"))

        if recs:
            rec_df = pd.DataFrame(recs, columns=["Dataset", "Recommendation", "Rationale"])
            st.dataframe(rec_df, use_container_width=True)
        else:
            st.info("No specific governance recommendations triggered.")

        # ===== ADD DATASET CATALOG WITH METADATA =====
        st.divider()
        st.subheader("➕ Add Dataset Catalog with Metadata")
        with st.form("add_dataset_form"):
            dataset_name = st.text_input("Dataset Name")
            dataset_desc = st.text_area("Description")
            submit_dataset = st.form_submit_button("Add Dataset Catalog Entry")
            
            if submit_dataset and dataset_name and dataset_desc:
                try:
                    datasets_db = os.path.join(os.path.dirname(__file__), 'DATA', 'Datasets&Metadata_platform.db')
                    conn = sqlite3.connect(datasets_db)
                    cur = conn.cursor()
                    cur.execute('INSERT INTO datasets (name, description) VALUES (?, ?)',
                               (dataset_name, dataset_desc))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Dataset '{dataset_name}' created successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            elif submit_dataset:
                st.warning("Please fill in all fields.")