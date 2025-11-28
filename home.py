import streamlit as st
import pandas as pd
import numpy as np

#Run this file

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
        st.session_state.nav_radio = "Home"
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
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password123":
            st.session_state.logged_in = True
            st.success("Login successful! Redirecting to IT Operations...")
            # One-click redirect and balloons on next page render
            st.session_state.page = "IT Operations"
        else:
            st.error("Invalid credentials.")

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

        # Governance (storage & access based on metadata)
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