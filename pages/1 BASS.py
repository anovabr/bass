import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from data_loader import df_bass 
# Set the page configuration to wide mode
st.set_page_config(page_title="BASS (3 and 4)", layout="wide")

# Ensure all columns have a consistent type:
df_bass = df_bass.apply(lambda col: col.astype(str) if col.dtypes == object else col)

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

# Get columns for analysis
columns = [col for col in df_bass.columns if col.startswith("bass")]

# Main layout
col1, col2, col3 = st.columns(3)
with col1:
    bass_version = st.selectbox(
        "Results by BASS version",
        options=["None", "version"],  
        format_func=lambda x: {
            "version": "BASS version",
        }.get(x, x),
        index = 1
    )
with col2:
    default_index = columns.index("bass_inclusion_total") if "bass_inclusion_total" in columns else 0
    selected = st.selectbox(
        "Select a variable",
        options=columns,
        index=5
    )
with col3:
    group_var = st.selectbox(
        "Select a grouping variable",
        options=["None", "quest", "gender_c", "income_c", "momed_c", "dat_year"],  
        format_func=lambda x: {
            "quest": "Questionnaire (age)",
            "dat_year": "Year of the assessment",
            "gender_c": "Gender",
            "income_c": "Family income",
            "momed_c": "Mother's Education Level",
        }.get(x, x),
        index = 0
    )

# Sidebar with Dynamic Text
with st.sidebar:
    st.info(sidebar_texts.get(selected, sidebar_texts["default"]))

# Display the analysis results
if bass_version == "None":
    st.subheader(f"Descriptive statistics for {selected} (No Grouping)")
    st.dataframe(df_bass[selected].describe(), use_container_width=True)
else:
    # Create grouping based on selected variables
    grouping_vars = [bass_version]
    if group_var != "None":
        grouping_vars.append(group_var)

    # Convert numeric columns to float for calculations
    df_bass[selected] = pd.to_numeric(df_bass[selected], errors='coerce')

    grouped = df_bass.groupby(grouping_vars)[selected].describe()
    st.subheader(f"Descriptive statistics for {selected} grouped by {', '.join(grouping_vars)}")
    st.dataframe(grouped, use_container_width=True)
 
    # Perform ANOVA with multiple factors
    st.subheader(f"ANOVA: {selected} by grouping variables")
    formula_parts = [f"C({var})" for var in grouping_vars]
    formula = f"{selected} ~ " + " + ".join(formula_parts)
    model = smf.ols(formula, data=df_bass).fit(missing='drop')
    anova_table = sm.stats.anova_lm(model, typ=3)
    st.dataframe(anova_table, use_container_width=True)

    # Create and display the plot with grouping and stratification
    st.subheader(f"Bar Chart: {selected} by groups")
    
    # Add checkbox for swapping variables
    if len(grouping_vars) > 1:
        swap_vars = st.checkbox("Swap x-axis and grouping variables")
    else:
        swap_vars = False

    # Pre-aggregate the data with multiple grouping variables and calculate standard error
    agg_df_bass = (df_bass.groupby(grouping_vars)[selected]
             .agg(['mean', 'count', 'std'])
             .reset_index())
    
    # Calculate standard error
    agg_df_bass['stderr'] = agg_df_bass['std'] / np.sqrt(agg_df_bass['count'])
    
    # Convert all grouping variables to categorical
    for var in grouping_vars:
        agg_df_bass[var] = agg_df_bass[var].astype('category')
    
    # Determine x-axis and color variables based on swap setting
    if swap_vars and len(grouping_vars) > 1:
        x_var = grouping_vars[1]
        color_var = grouping_vars[0]
    else:
        x_var = grouping_vars[0]
        color_var = grouping_vars[1] if len(grouping_vars) > 1 else None

    # Create the plot with appropriate grouping
    fig = px.bar(
        agg_df_bass,
        x=x_var,
        y='mean',
        error_y='stderr',
        color=color_var,
        title=f"Mean {selected} by {', '.join(grouping_vars)}",
        barmode="group"
    )

    # Update layout to improve appearance
    fig.update_layout(
        xaxis_title=x_var,
        yaxis_title=f"Mean {selected}",
        xaxis_tickangle=-45,
        xaxis={'type': 'category', 
              'categoryorder': 'array', 
              'categoryarray': sorted(agg_df_bass[x_var].unique())},
        showlegend=True,
        legend_title_text=color_var if color_var else None,
    )

    # Update error bar appearance to minimize overlap
    fig.update_traces(
        error_y=dict(
            thickness=1.5,
            width=6,
            color='rgba(0,0,0,0.3)'
        )
    )

    st.plotly_chart(fig, use_container_width=True)