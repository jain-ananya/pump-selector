import streamlit as st
import pandas as pd

# Load the new pump data
# Ensure the file is named 'clean_pumps.csv' on GitHub
df = pd.read_csv('clean_pumps.csv')

# Clean column names (removes spaces like the previous error)
df.columns = df.columns.str.strip()

st.title("CRI Pump Selector")
st.write("Find the perfect CRI pump for your home or farm.")

# Sidebar Filters
st.sidebar.header("Filter by Type")
pump_types = df['Pump Type'].unique()
selected_type = st.sidebar.multiselect("Select Pump Category", options=pump_types, default=pump_types)

st.sidebar.header("Enter Your Requirements")
depth = st.sidebar.number_input("Borewell/Well Depth (meters)", min_value=0, value=50)
tank_height = st.sidebar.number_input("Overhead Tank Height (meters)", min_value=0, value=10)

# Calculate Total Head
total_head = (depth + tank_height) * 1.10
st.info(f"Your requirement: ~**{total_head:.2f} meters** of vertical lift.")

# Filtering Logic
# 1. Filter by User Selected Pump Types
# 2. Filter by Max Head (The pump's Max Head must be greater than our requirement)
recommendations = df[
    (df['Pump Type'].isin(selected_type)) & 
    (df['Max Head (m)'] >= total_head)
]

# Display Results
st.subheader("Matching CRI Models")
if not recommendations.empty:
    # Sort by HP (lowest HP first for efficiency)
    recommendations = recommendations.sort_values(by='HP')
    
    # Select specific columns to show the user
    display_cols = ['Series', 'Model', 'HP', 'Max Head (m)', 'Outlet Size (mm)', 'Applications']
    
    st.dataframe(recommendations[display_cols], hide_index=True)
    
    # Recommendation Highlight
    best = recommendations.iloc[0]
    st.success(f"**Top Pick:** {best['Series']} {best['Model']} ({best['HP']} HP)")
    st.caption(f"**Best for:** {best['Applications']}")
else:
    st.error("No pumps found for this depth. Please reduce the depth or contact your CRI dealer.")
