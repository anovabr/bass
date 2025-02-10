import streamlit as st
import pandas as pd
import plotly.express as px
from tableone import TableOne
from data_loader import df  # Load dataset from a CSV file

# Set the page configuration to wide mode
st.set_page_config(page_title="Descriptive Statistics", layout="wide")

# Ensure all columns have a consistent type:
df = df.apply(lambda col: col.astype(str) if col.dtypes == object else col)

# Descriptive analysis based on selection
columns = [col for col in df.columns if col.startswith("bass") and "text" not in col.lower() and not any(char.isdigit() for char in col)]

# Dictionary with custom messages for sidebar
sidebar_texts = {
    "bass_inclusion_total": """  
    **Inclusion Criterion in BASS**  
    This section assesses whether the child's speech is understandable. It includes:  
    - **Understanding**: Can you understand what the child says?  
    - **Clarity**: Can other people understand the child?  
    - **Concerns**: Are there any concerns about the child's speech?  
    """,
    "bass_phonemes_total": """ 
    **Phoneme Recognition in BASS**  
    This score represents the total phoneme recognition ability of the child.  
    The child was assessed on their ability to pronounce different phonemes, such as:   
    
    - **b** as in *baby, bottle, or ball*  
    - **p** as in *paw, pig, or puppy*  
    - **m** as in *mama, more, or monkey*  
    - **n** as in *nose, night, or no*  
    - **d** as in *doll, dog, or dada*  
    - **h** as in *hop, help, or hair*  
    - **w** as in *want, wow, or waffle*  

    More complex phonemes include **ch, sh, kw, th, v, s, r, l, z, and f** in different word contexts.
    """,
    "bass_subtotal": "This is the overall sum of BASS performance across multiple domains.",
    "default": "Select a variable to see more information."
}

# Create Tabs
tab1, tab2 = st.tabs(["Filtered Analysis", "Descriptive Statistics for All"])

### **Tab 1: Filtered Descriptive Analysis**
with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        bass_version = st.selectbox(
            "Select BASS Version",
            options=["All"] + df["version"].unique().tolist(),  # ADDED dynamic version selection
            format_func=lambda x: f"BASS Version {x}" if x != "All" else "All Versions"
        )

    with col2:
        group_var = st.selectbox(
            "Select a grouping variable or 'None' for no grouping",
            options=["None", "quest", "gender", "momed", "dat_year"],  
            format_func=lambda x: {
                "dat_year": "Year of the assessment",
                "quest": "Questionnaire (age)",
                "gender": "Gender",
                "version": "BASS Version",
                "momed": "Mother's Education Level",
            }.get(x, x)  
        )

    with col3:
        default_index = columns.index("bass_inclusion_total") if "bass_inclusion_total" in columns else 0
        selected = st.selectbox(
            "Select a variable",
            options=columns,
            index=default_index
        )

    # **Sidebar Box with Dynamic Text**
    with st.sidebar:
        st.info(sidebar_texts.get(selected, sidebar_texts["default"]))

    # **Filter Data by Selected BASS Version**
    if bass_version == "All":
        filtered_df = df  # No filtering applied
    else:
        filtered_df = df[df["version"] == bass_version]  # Apply version filter

    # Display the analysis results
    if group_var == "None":
        st.subheader(f"Descriptive statistics for {selected} (No Grouping) - {bass_version}")
        st.dataframe(filtered_df[selected].describe(), use_container_width=True)
    else:
        grouped = filtered_df.groupby(group_var)[selected].describe()
        st.subheader(f"Descriptive statistics for {selected} grouped by {group_var} - {bass_version}")
        st.dataframe(grouped, use_container_width=True)

        # Only create and display the plot if there's a grouping variable
        st.subheader(f"Bar Chart: {selected} by {group_var}, clustered by BASS Version")
        
        # Pre-aggregate the data
        agg_df = filtered_df.groupby([group_var, "version"])[selected].agg(['mean', 'count']).reset_index()

        fig = px.bar(
            agg_df,
            x=group_var,
            y=('mean'),
            color="version",
            title=f"Mean {selected} by {group_var} (Grouped by BASS Version)",
            barmode="group"
        )

        fig.update_layout(
            xaxis_title=group_var,
            yaxis_title=f"Mean {selected}",
            legend_title="BASS Version",
            xaxis_tickangle=-45
        )

        st.plotly_chart(fig, use_container_width=True)

### **Tab 2: Descriptive Statistics for All Variables**
with tab2:
    st.subheader("Descriptive Statistics for All Variables")

    # Use `TableOne` to generate a summary table
    table = TableOne(df, columns=columns, groupby="quest", missing=True)

    # Convert `TableOne` summary into DataFrame format
    table_df = table.tableone.reset_index()

    # Display the full descriptive statistics table
    st.dataframe(table_df, use_container_width=True)
