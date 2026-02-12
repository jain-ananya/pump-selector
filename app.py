import streamlit as st
import pandas as pd

st.title("CRI Pump Selector")

# Load pump database
df = pd.read_csv("pumps.csv")

st.sidebar.header("Enter Requirements")

bore_depth = st.sidebar.number_input("Bore Depth (m)", 1, 500)
water_level = st.sidebar.number_input("Water Level (m)", 0, 500)
tank_height = st.sidebar.number_input("Tank Height (m)", 0, 200)
pipe_length = st.sidebar.number_input("Pipe Length (m)", 0, 500)

usage = st.sidebar.selectbox(
    "Usage Type",
    ["Domestic", "Agriculture", "Drip"]
)

phase = st.sidebar.selectbox(
    "Power Phase",
    ["Single", "Three"]
)

# Calculations
vertical_lift = bore_depth - water_level
friction_loss = pipe_length * 0.1
total_head = vertical_lift + tank_height + friction_loss

if usage == "Domestic":
    flow = 25
elif usage == "Agriculture":
    flow = 80
else:
    flow = 40

st.subheader("Calculated Requirements")
st.write("Total Head:", round(total_head,2),"m")
st.write("Required Flow:", flow,"L/min")

# Filter Pumps
results = df[
    (df.MinHead <= total_head) &
    (df.MaxHead >= total_head) &
    (df.MinFlow <= flow) &
    (df.MaxFlow >= flow) &
    (df.Phase == phase)
]

st.subheader("Recommended Pumps")

if len(results) == 0:
    st.warning("No matching pumps found")
else:
    st.dataframe(results)
