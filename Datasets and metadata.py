import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Governance Dashboard", layout="wide")
st.title("🗄️ Data Governance & Metadata Discovery")

# Mock dataset catalog with metadata
rng = np.random.default_rng(7)
owners = ["Cyber", "IT", "Analytics", "Finance", "HR"]
sources = ["S3", "Azure Blob", "On-Prem NAS", "Snowflake", "Google Drive"]

df = pd.DataFrame({
    "dataset": [f"ds_{i}" for i in range(1, 31)],
    "owner": rng.choice(owners, size=30),
    "source": rng.choice(sources, size=30),
    "size_gb": rng.uniform(1, 200, 30).round(1),
    "rows_millions": rng.uniform(0.1, 100, 30).round(1),
    "dependencies": rng.integers(0, 5, 30),
    "last_accessed": rng.choice(pd.date_range("2025-07-01", "2025-11-30", freq="D"), size=30),
    "pii": rng.choice([True, False], size=30, p=[0.4, 0.6])
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

