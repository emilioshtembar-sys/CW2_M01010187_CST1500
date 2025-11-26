import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Login Page", layout="centered")
st.title("🔐 Login")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login form
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        # Replace with your own authentication logic
        if username == "admin" and password == "password123":
            st.session_state.authenticated = True
            st.success("Login successful! You can now access other dashboards.")
            st.balloons()
        else:
            st.error("Invalid credentials. Please try again.")

# Show login status
if st.session_state.authenticated:
    st.info("You are logged in. Use the sidebar to navigate to other pages.")
else:
    st.warning("Not logged in. Please enter your credentials.")