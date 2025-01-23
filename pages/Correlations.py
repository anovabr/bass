import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_loader import df # Load the dataset from a CSV file located in the main folder

# Set page configuration
st.set_page_config(page_title="Correlations", layout="wide")

# App title
st.title("Scatterplot Generator")
st.write("Select two variables from the listboxes below to generate a scatterplot.")

# Create two columns for the listboxes
col1, col2 = st.columns(2)

# Listbox for selecting the X-axis variable
with col1:
    x_var = st.selectbox(
        "Select X-axis Variable", 
        options=df.columns,
        index=list(df.columns).index("bass_subtotal")  # Default to "bass_subtotal"
    )

# Listbox for selecting the Y-axis variable
with col2:
    y_var = st.selectbox("Select Y-axis Variable", options=df.columns)

# Display scatterplot if variables are selected
if x_var and y_var:
    st.subheader(f"Scatterplot: {x_var} vs {y_var}")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax)
    ax.set_title(f"{x_var} vs {y_var}")
    st.pyplot(fig)
