import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")
st.title("🛡️ Cybersecurity: Incident Response Bottleneck")

# Mock data (replace with SIEM/IR export)
rng = np.random.default_rng(42)
df = pd.DataFrame({
    "category": rng.choice(["Phishing", "Malware", "Ransomware"], 300, p=[0.5, 0.3, 0.2]),
    "status": rng.choice(["Open", "Resolved", "In Progress"], 300),
    "resolution_days": rng.integers(1, 15, 300)
})

# KPIs
col1, col2 = st.columns(2)
col1.metric("Phishing incidents", (df["category"] == "Phishing").sum())
col2.metric("High-severity backlog", len(df[(df["category"]=="Phishing") & (df["status"]!="Resolved")]))

# Chart: resolution time by category
st.subheader("Average resolution time by category")
avg_res = df.groupby("category")["resolution_days"].mean()
st.bar_chart(avg_res)

# Insight
worst = avg_res.idxmax()
st.info(f"Bottleneck: {worst} cases take longest to resolve.")