import streamlit as st
import pandas as pd
from tableone import TableOne
from data_loader import df # Load the dataset from a CSV file located in the main folder


# Set the page configuration to wide mode (makes the app and tables wider)
st.set_page_config(page_title="Descriptive Statistics", layout="wide")

# Ensure all columns have a consistent type:
# Convert columns with 'object' (string-like) types to strings and keep other columns unchanged.
df = df.apply(lambda col: col.astype(str) if col.dtypes == object else col)

# Filter columns that start with "bass" and do not contain "text"
# These will be the options available for analysis in the selectbox.
columns = [col for col in df.columns if col.startswith("bass") and "text" not in col.lower()]

# Create two side-by-side columns for user inputs (grouping variable and analysis variable)
col1, col2 = st.columns(2)

# Place the first selectbox in the first column
# This allows the user to choose a grouping variable or "None" for no grouping.
with col1:
    group_var = st.selectbox("Select a grouping variable (or 'None' for no grouping)", options=["None", "quest", "gender", "momed"])

# Place the second selectbox in the second column
# This allows the user to select a numeric variable for descriptive statistics.
with col2:
    default_index = columns.index("bass_subtotal")  # Find the index of the default value
    selected = st.selectbox("Select a variable", options=columns, index=default_index)  # Set default 

# Display the analysis results
if group_var == "None":
    # If no grouping variable is selected, show overall descriptive statistics for the selected column
    st.subheader(f"Descriptive statistics for {selected} (No Grouping)")
    st.write(df[selected].describe())
else:
    # If a grouping variable is selected, group the data by the selected variable
    # Then calculate descriptive statistics for the chosen column within each group
    grouped = df.groupby(group_var)[selected].describe()
    st.subheader(f"Descriptive statistics for {selected} grouped by {group_var}")
    st.write(grouped)

# Generate and display the descriptive statistics table for all selected variables
st.subheader("Descriptive Statistics for All Variables")

# Use the `TableOne` library to generate a summary table
# Group the data by the "quest" variable and include missing data in the analysis.
table = TableOne(df, columns=columns, groupby="quest", missing=True)

# Convert the `TableOne` summary into a DataFrame format to display it in Streamlit
table_df = table.tableone.reset_index()

# Use `st.dataframe` to render the summary table interactively
st.dataframe(table_df)
