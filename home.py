import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from data_loader import df_bass

# Set page configuration
st.set_page_config(
    page_title="BASS Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
    }
    .info-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown('<p class="main-header">BASS Statistical Analysis Dashboard</p>', unsafe_allow_html=True)

# Introduction boxes
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="background-color:#f8f9fa; padding:20px; border-radius:10px; border-left:5px solid #007bff;">
            <h3>Dataset Overview</h3>
            <p><b>BASS V.3 and V.4:</b> 1,306 children</p>
            <p><b>CastIron complete dataset:</b> 10,176 children</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background-color:#f8f9fa; padding:20px; border-radius:10px; border-left:5px solid #28a745;">
            <h3>About This Tool</h3>
            <p>This experimental application enables statistical analysis, result comparison, and visual exploration through graphs and tables. All results can be exported to Excel, and data was distributed via email.</p>
        </div>
    """, unsafe_allow_html=True)


# GIF Section
st.markdown("""
    <div style="background-color:white; padding:20px; border-radius:10px; margin:20px 0;">
        <h3>Fighting Ducks</h3>
        <img src="https://media1.giphy.com/media/Xexx4Lje6D3cwQWUvY/200w.gif?cid=6c09b952sowzjq4z1yqqf5vkc4od79ad7ttxn519rjuqkmt4&ep=v1_gifs_search&rid=200w.gif&ct=g" 
            style="width:20%; 
            max-width:800px; 
            margin:20px auto; 
            display:block;">
    </div>
""", unsafe_allow_html=True)