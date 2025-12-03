import streamlit as st
import pandas as pd

st.title("Pandas demo (safe file name)")

# Small valid dataframe (matching lengths)
df = pd.DataFrame(
    {
        'name': ["Luke", "Matt", "Emilio"],
        'age': [10, 20, 30]
    }
)

st.subheader("Sample DataFrame")
st.dataframe(df)

st.divider()
st.write("This demo replaces the old `pandas.py` file which shadowed the real `pandas` package.")
