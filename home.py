import streamlit as st
import pandas as pd
import numpy as np
import os


# One-time email gating: saves to project DATA/user_email.txt
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(BASE_DIR, 'DATA')
EMAIL_FILE = os.path.join(DATA_DIR, 'user_email.txt')

if 'email_saved' not in st.session_state:
    st.session_state.email_saved = False

if not st.session_state.email_saved:
    st.markdown("### Welcome — please allow access by entering your email to continue")
    email_input = st.text_input('Email address')
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Save and continue'):
            if email_input and '@' in email_input:
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(EMAIL_FILE, 'w', encoding='utf-8') as f:
                    f.write(email_input)
                st.session_state.email_saved = True
                st.experimental_rerun()
            else:
                st.error('Please enter a valid email address.')
    with col2:
        if st.button('Cancel'):
            st.stop()

# If there's already a saved email on disk, mark session as saved
if not st.session_state.email_saved:
    try:
        if os.path.exists(EMAIL_FILE):
            with open(EMAIL_FILE, 'r', encoding='utf-8') as f:
                saved = f.read().strip()
            if saved:
                st.session_state.email_saved = True
    except Exception:
        pass

if not st.session_state.email_saved:
    st.stop()

st.set_page_config(page_title="Domain Dashboards", layout="wide", initial_sidebar_state="expanded")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Login", "IT Operations", "Cybersecurity", "Datasets and Metadata"]
)


# ---------------- Home Page ----------------
if page == "Home":
    st.title("📊 Domain Insight Dashboards")
    st.write("Welcome! Use the sidebar to access dashboards.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=200)

# ---------------- Login Page ----------------
elif page == "Login":
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    if st.button("Login"):
        if username == "admin" and password == "Magic123#":
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting to IT Operations...")
            st.session_state.page = "IT Operations"   # 👈 force redirect
            st.experimental_rerun()
        else:
            st.error("Invalid credentials.")


# ---------------- IT Operations Page ----------------
elif page == "IT Operations":
    st.title("🛠️ IT Operations Dashboard")
    st.write("Service desk performance analysis goes here.")

    rng = np.random.default_rng(11)
    df = pd.DataFrame({
        "assignee": rng.choice(["Alex","Bianca","Chen","Dev"], 50),
        "resolution_hours": rng.integers(1, 72, 50),
        "tickets": rng.integers(1, 20, 50)  # mock ticket counts
    })

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Tickets", len(df))
    col2.metric("Avg Resolution (hrs)", round(df["resolution_hours"].mean(), 1))
    col3.metric("Max Resolution (hrs)", df["resolution_hours"].max())

    st.divider()

    # Full table preview
    st.subheader("Service Desk Records")
    st.dataframe(df, use_container_width=True)

    # Scatter chart: tickets vs resolution hours
    st.subheader("Tickets vs Resolution Hours")
    st.scatter_chart(df, x="tickets", y="resolution_hours")

    # Governance Recommendations
    st.subheader("Governance Recommendations")
    recs = []
    for _, r in df.iterrows():
        if r["resolution_hours"] > 48:
            recs.append((r["assignee"], "Workload balancing", f"Resolution {r['resolution_hours']} hrs"))
        if r["tickets"] > 15 and r["resolution_hours"] > 30:
            recs.append((r["assignee"], "Process optimization", f"{r['tickets']} tickets, avg {r['resolution_hours']} hrs"))
    if recs:
        rec_df = pd.DataFrame(recs, columns=["Assignee", "Recommendation", "Rationale"])
        st.dataframe(rec_df, use_container_width=True)
    else:
        st.info("No specific governance recommendations triggered.")

# ---------------- Cybersecurity Page ----------------
elif page == "Cybersecurity":
    st.title("🛡️ Cybersecurity Dashboard")
    st.write("Phishing spike analysis and response bottlenecks go here.")

    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "category": rng.choice(["Phishing", "Malware", "Ransomware"], 100, p=[0.5, 0.3, 0.2]),
        "resolution_days": rng.integers(1, 15, 100),
        "incidents": rng.integers(1, 10, 100)  # mock incident counts
    })

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Incidents", len(df))
    col2.metric("Avg Resolution (days)", round(df["resolution_days"].mean(), 1))
    col3.metric("Phishing %", round((df["category"].eq("Phishing").mean())*100, 1))

    st.divider()

    # Full table preview
    st.subheader("Incident Records")
    st.dataframe(df, use_container_width=True)

    # Scatter chart: incidents vs resolution days
    st.subheader("Incidents vs Resolution Days")
    st.scatter_chart(df, x="incidents", y="resolution_days")

    # Governance Recommendations
    st.subheader("Governance Recommendations")
    recs = []
    for _, r in df.iterrows():
        if r["category"] == "Phishing" and r["resolution_days"] > 10:
            recs.append((r["category"], "Enhanced phishing training", f"Resolution {r['resolution_days']} days"))
        if r["category"] == "Ransomware" and r["incidents"] > 5:
            recs.append((r["category"], "Strict containment protocols", f"{r['incidents']} ransomware incidents"))
        if r["resolution_days"] > 12:
            recs.append((r["category"], "Escalation required", f"Resolution {r['resolution_days']} days"))
    if recs:
        rec_df = pd.DataFrame(recs, columns=["Category", "Recommendation", "Rationale"])
        st.dataframe(rec_df, use_container_width=True)
    else:
        st.info("No specific governance recommendations triggered.")




# ---------------- Datasets and Metadata Page ----------------
elif page == "Datasets and Metadata":
    st.title("📂 Datasets and Metadata")
    st.write("Information about datasets used in the dashboards.")
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=200)

    # Mock dataset catalog with metadata
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
    col4.metric("PII datasets", df["pii"].sum())

    st.divider()

    # Table preview
    st.subheader("Dataset Catalog with Metadata")
    st.dataframe(df, use_container_width=True)

    # Chart: dependencies vs size
    st.subheader("Dependencies vs Size")
    st.scatter_chart(df, x="dependencies", y="size_gb")

    # Chart: average dependencies by source
    st.subheader("Average Dependencies by Source")
    dep_by_source = df.groupby("source")["dependencies"].mean().sort_values(ascending=False)
    st.bar_chart(dep_by_source)

    # Governance Recommendations
    st.subheader("Governance Recommendations")
    recs = []
    for _, r in df.iterrows():
        days_since_access = (pd.to_datetime("2025-11-30") - r["last_accessed"]).days
        if r["size_gb"] > 100 and r["dependencies"] < 2 and days_since_access > 30:
            recs.append((r["dataset"], "Archive/Cold storage", f"{r['size_gb']} GB, deps={r['dependencies']}, last accessed {r['last_accessed'].date()}"))
        if r["pii"] and r["dependencies"] >= 3:
            recs.append((r["dataset"], "Strict governance (access controls, audits)", f"PII=True, deps={r['dependencies']}"))
        if r["rows_millions"] > 50 and r["source"] in ["S3", "Azure Blob"]:
            recs.append((r["dataset"], "Storage tier optimization", f"Rows={r['rows_millions']}M on {r['source']}"))

    if recs:
        rec_df = pd.DataFrame(recs, columns=["Dataset", "Recommendation", "Rationale"])
        st.dataframe(rec_df, use_container_width=True)
    else:
        st.info("No specific governance recommendations triggered.")