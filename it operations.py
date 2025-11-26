import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="IT Operations Dashboard", layout="wide")
st.title("🛠️ IT Operations: Service Desk Performance")

# Mock tickets
rng = np.random.default_rng(11)
df = pd.DataFrame({
    "assignee": rng.choice(["Alex","Bianca","Chen","Dev"], 200),
    "status": rng.choice(["New","In Progress","Waiting for User","Resolved"], 200),
    "resolution_hours": rng.integers(1, 72, 200)
})

# KPIs
col1, col2 = st.columns(2)
col1.metric("Tickets", len(df))
col2.metric("Avg resolution (hrs)", round(df["resolution_hours"].mean(),1))

# Chart: resolution by status
st.subheader("Resolution time by status")
status_avg = df.groupby("status")["resolution_hours"].mean()
st.bar_chart(status_avg)

# Chart: resolution by assignee
st.subheader("Resolution time by assignee")
assignee_avg = df.groupby("assignee")["resolution_hours"].mean()
st.bar_chart(assignee_avg)

# Insight
worst_status = status_avg.idxmax()
st.warning(f"Bottleneck: '{worst_status}' causes the greatest delay.")