import streamlit as st
import pandas as pd
from data_loader import df

# Set page configuration
st.set_page_config(page_title="BASS Dashboard", layout="wide")

# Main page content
st.title("Welcome to the BASS Dashboard")

# DataFrame info
n_rows, n_columns = df.shape

# Two colored boxes side by side
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="background-color:#ffddc1; padding:15px; border-radius:10px;">
            <h4 style="color:#333333;">📌 How to Use this app</h4>
            <p style="color:#555555;">Use the sidebar to navigate between pages and explore the app's features.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="background-color:#c1e1ff; padding:15px; border-radius:10px;">
            <h4 style="color:#333333;">🐍 Made in Python with Streamlit</h4>
            <p style="color:#555555;">Reach out to me at luisfc@gmail.com.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Add a box with DataFrame information
st.markdown(
    f"""
    <div style="background-color:#d4edda; padding:15px; border-radius:10px; margin-top:20px;">
        <h4 style="color:#155724;">ℹ️ DataFrame Information</h4>
        <p style="color:#155724;">The current DataFrame has <b>{n_rows}</b> rows and <b>{n_columns}</b> columns.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
