import streamlit as st
import pandas as pd
import io

st.title("CRI Pump Selector")

# ---------------------------------------------------------
# 1. EMBEDDED CSV DATA
# ---------------------------------------------------------
# I have normalized the data from the CRI Catalog into the format your app expects.
# Flow is converted to L/min (1 lps = 60 L/min).
# Phase is standardized to "Single" or "Three".
csv_data = """Series,Model,MinHead,MaxHead,MinFlow,MaxFlow,Phase
LENA,80mm Borewell,0,156,0,90,Single
LENA+,85mm Borewell,0,214,0,54,Single
ZUNO Lite,80mm Borewell,0,70,0,90,Single
GENIE,100mm Borewell (1Ph),0,568,0,420,Single
GENIE,100mm Borewell (3Ph),0,568,0,420,Three
ZUNO,100mm Borewell (1Ph),0,220,0,420,Single
ZUNO,100mm Borewell (3Ph),0,220,0,420,Three
STEELIX,100mm SS Borewell (1Ph),0,487,0,183,Single
STEELIX,100mm SS Borewell (3Ph),0,487,0,183,Three
LTK,Vertical Openwell,0,89,0,96,Single
Plano/CSS,Horizontal Openwell (1Ph),0,56,0,1020,Single
Plano/CSS,Horizontal Openwell (3Ph),0,56,0,1020,Three
VIRAT,Centrifugal Monoblock (1Ph),0,60,0,1080,Single
VIRAT,Centrifugal Monoblock (3Ph),0,60,0,1080,Three
JTS,SS Monoblock,0,40,0,62,Single
AJ,Deepwell Jet,0,92,0,50,Single
SHALO,Selfpriming Jet,0,47,0,56,Single
SELFY,Regenerative Selfpriming,0,55,0,64,Single
Royale,Monoblock,0,100,0,63,Single
"""

# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------
# Use io.StringIO to treat the string like a file
df = pd.read_csv(io.StringIO(csv_data))

st.sidebar.header("Enter Requirements")

# ---------------------------------------------------------
# 3. INPUTS
# ---------------------------------------------------------
bore_depth = st.sidebar.number_input("Bore Depth (m)", 1, 500, value=30)
water_level = st.sidebar.number_input("Water Level (m)", 0, 500, value=10)
tank_height = st.sidebar.number_input("Tank Height (m)", 0, 200, value=5)
pipe_length = st.sidebar.number_input("Pipe Length (m)", 0, 500, value=40)

usage = st.sidebar.selectbox(
    "Usage Type",
    ["Domestic", "Agriculture", "Drip"]
)

phase = st.sidebar.selectbox(
    "Power Phase",
    ["Single", "Three"]
)

# ---------------------------------------------------------
# 4. CALCULATIONS
# ---------------------------------------------------------
# Basic head calculation
vertical_lift = bore_depth - water_level # Assuming pump is at bore bottom, strictly lift is usually Total Head = Depth + Elevation + Friction
# However, standard simple calculation is usually: Total Static Head = (Depth to water) + (Tank Height)
# If pump is submersible, it pushes from the bottom.
# Let's stick to your formula logic:
total_head = bore_depth + tank_height + (pipe_length * 0.1) 

if usage == "Domestic":
    flow = 25
elif usage == "Agriculture":
    flow = 80
else:
    flow = 40

st.subheader("Calculated Requirements")
st.write(f"Total Head Required: **{round(total_head, 2)} m**")
st.write(f"Required Flow: **{flow} L/min**")

# ---------------------------------------------------------
# 5. FILTERING
# ---------------------------------------------------------
# Filter Logic:
# 1. Pump MaxHead must be > required Head
# 2. Pump MaxFlow must be > required Flow
# 3. Phase must match
results = df[
    (df.MaxHead >= total_head) &
    (df.MaxFlow >= flow) &
    (df.Phase == phase)
]

st.subheader("Recommended Pumps")

if len(results) == 0:
    st.warning("No matching pumps found for these requirements.")
else:
    # Formatting for cleaner display
    st.success(f"Found {len(results)} matching pumps!")
    st.dataframe(results.style.format({"MaxHead": "{:.1f} m", "MaxFlow": "{:.1f} L/min"}))

    # Optional: Show best match (lowest sufficient MaxHead to save energy)
    best_match = results.sort_values(by="MaxHead").iloc[0]
    st.info(f"**Best Match:** {best_match['Series']} - {best_match['Model']}")
