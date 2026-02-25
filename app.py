import streamlit as st
import pandas as pd

st.title("CRI Pump Selector")

# ---------- LOAD DATA ----------
df = pd.read_csv("clean_pumps.csv")

# convert numeric columns
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="ignore")

# ---------- INPUT ----------
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
    [1, 3]
)

# ---------- CALCULATIONS ----------
vertical_lift = bore_depth - water_level
friction_loss = pipe_length * 0.1
total_head = vertical_lift + tank_height + friction_loss

if usage == "Domestic":
    flow = 1
elif usage == "Agriculture":
    flow = 3
else:
    flow = 2

st.subheader("Calculated Requirements")
st.write("Total Head:", round(total_head,2),"m")
st.write("Required Flow:", flow,"m³/hr")

# ---------- FILTER ----------
results = df[
    (df["min head"] <= total_head) &
    (df["max head"] >= total_head) &
    (df["min flow"] <= flow) &
    (df["max flow"] >= flow) &
    (df["phase"] == phase)
]

results = results.sort_values(by="power")

# ---------- OUTPUT ----------
st.subheader("Recommended Pumps")

if results.empty:
    st.warning("No suitable pump found")
else:
    st.dataframe(results)
