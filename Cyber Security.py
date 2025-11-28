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


# ---------------- Cybersecurity: Phishing Spike Analysis ----------------
st.header("🛡️ Cybersecurity: Phishing Spike Analysis & Response Bottlenecks")

rng = np.random.default_rng(42)
df_cyber = pd.DataFrame({
    "category": rng.choice(["Phishing", "Malware", "Ransomware"], 100, p=[0.5, 0.3, 0.2]),
    "resolution_days": rng.integers(1, 15, 100),
    "date": rng.choice(pd.date_range("2025-09-01", "2025-11-30", freq="D"), 100)
})

# Average resolution time by category
summary_cyber = df_cyber.groupby("category")["resolution_days"].agg(["count","mean"]).reset_index()
summary_cyber["Insight"] = summary_cyber.apply(
    lambda r: "Spike + slow response" if r["category"]=="Phishing" else "Normal",
    axis=1
)
st.subheader("Resolution Bottlenecks by Threat Category")
st.dataframe(summary_cyber, use_container_width=True)
st.bar_chart(summary_cyber.set_index("category")["mean"])

# Trend chart: phishing incidents over time
phishing_trend = df_cyber[df_cyber["category"]=="Phishing"].groupby("date").size().reset_index(name="count")
st.subheader("Phishing Incident Trend Over Time")
st.line_chart(phishing_trend.set_index("date")["count"])
