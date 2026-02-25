import streamlit as st
import pandas as pd

# Load the pump data
df = pd.read_csv('clean_pumps.csv')

st.title("CRI Pump Selector - Hardware Shop Helper")
st.write("Enter your requirements below to find the best CRI pump for your borewell.")

# Sidebar for Inputs
st.sidebar.header("User Requirements")
depth = st.sidebar.number_input("Borewell Depth (meters)", min_value=0, value=50)
tank_height = st.sidebar.number_input("Overhead Tank Height (meters)", min_value=0, value=10)
phase_req = st.sidebar.selectbox("Phase", options=[1, 3], index=0)

# Calculate Total Head (adding 10% for pipe friction)
total_head = (depth + tank_height) * 1.10
st.info(f"Calculated Total Head Requirement: **{total_head:.2f} meters**")

# Filtering Logic
# 1. Filter by Phase
# 2. Total Head must be between min head and max head
recommendations = df[
    (df['phase'] == phase_req) & 
    (df['min head'] <= total_head) & 
    (df['max head'] >= total_head)
]

# Display Results
st.subheader("Recommended Pumps")
if not recommendations.empty:
    # Sort by power (lower power is usually more energy efficient for same head)
    recommendations = recommendations.sort_values(by='power')
    
    # Rename columns for better readability
    display_df = recommendations.rename(columns={
        'power': 'Power (HP)',
        'stage': 'Stages',
        'max head': 'Max Head (m)',
        'max flow': 'Max Flow',
        'del size': 'Pipe Size (mm)'
    })
    
    st.write(f"We found **{len(display_df)}** matching pumps:")
    st.dataframe(display_df[['Power (HP)', 'Stages', 'Max Head (m)', 'Pipe Size (mm)']])
    
    # Best Pick
    best_pick = recommendations.iloc[0]
    st.success(f"**Best Recommendation:** {best_pick['power']} HP Pump with {best_pick['stage']} stages.")
else:
    st.error("No pumps found for this depth. Please check the depth or consult a technician.")
