import streamlit as st
import pandas as pd
import time

# 1. Page Configuration & Custom CSS for Card Design
st.set_page_config(page_title="CRI Pump Selector", layout="wide")

st.markdown("""
    <style>
    .pump-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #ddd;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .pump-card:hover {
        transform: scale(1.02);
        border-color: #e63946;
    }
    .top-badge {
        background-color: #e63946;
        color: white;
        padding: 2px 8px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('clean_pumps.csv')
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except:
    st.error("Please ensure 'clean_pumps.csv' is in your GitHub repository.")
    st.stop()

# 3. Sidebar Inputs
st.sidebar.image("https://www.crigroups.com/wp-content/uploads/2018/05/logo.png", width=150) # Use CRI logo
st.sidebar.header("Step 1: Selection")
pump_types = df['Pump Type'].unique()
selected_type = st.sidebar.multiselect("Pump Category", options=pump_types, default=pump_types[0])

st.sidebar.header("Step 2: Well Dimensions")
depth = st.sidebar.number_input("Borewell/Well Depth (meters)", min_value=0, value=40)
tank_height = st.sidebar.number_input("Overhead Tank Height (meters)", min_value=0, value=10)

# 4. Calculation Logic
total_head = (depth + tank_height) * 1.10

# 5. Main UI Header
st.title("🚀 CRI Pump Smart Selector")
st.write(f"Finding recommendations for a **{total_head:.1f}m** head requirement.")

# Animated loading indicator
with st.spinner('Analyzing pump performance curves...'):
    time.sleep(1) # Simulation for animation effect
    recommendations = df[
        (df['Pump Type'].isin(selected_type)) & 
        (df['Max Head (m)'] >= total_head)
    ].sort_values(by=['HP', 'Max Head (m)'])

# 6. Top 3 Suggestions (Card Style)
if not recommendations.empty:
    st.subheader("⭐ Top 3 Recommendations")
    top_3 = recommendations.head(3)
    
    cols = st.columns(3)
    for i, (index, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div class="pump-card">
                    <span class="top-badge">Rank #{i+1}</span>
                    <h3>{row['Series']} {row['Model']}</h3>
                    <p><b>Power:</b> {row['HP']} HP ({row['kW']} kW)</p>
                    <p><b>Max Head:</b> {row['Max Head (m)']} meters</p>
                    <p><b>Outlet:</b> {row['Outlet Size (mm)']} mm</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"View Specs for {row['Model']}", key=f"btn_{row['Model']}"):
                st.info(f"**Application:** {row['Applications']}")

    # 7. Comparison View
    st.divider()
    st.subheader("🔍 Pump Comparison Tool")
    compare_models = st.multiselect("Select pumps to compare side-by-side:", 
                                     options=recommendations['Model'].tolist(),
                                     default=top_3['Model'].tolist()[:2])
    
    if compare_models:
        compare_df = df[df['Model'].isin(compare_models)].set_index('Model')
        st.table(compare_df[['Series', 'HP', 'kW', 'Max Head (m)', 'Outlet Size (mm)']])

else:
    st.error("No exact matches found. Try reducing the depth or selecting another pump category.")

# 8. Contact Section
st.sidebar.divider()
st.sidebar.subheader("📞 Need Expert Help?")
st.sidebar.write("Get a professional quote or technical advice.")

# Official CRI contact info from catalog
st.sidebar.link_button("Chat on WhatsApp", "https://wa.me/919500401115")
st.sidebar.write("**Toll Free:** 1800 121 1243")

if st.sidebar.button("Show Shop Location"):
    st.sidebar.success("📍 Your Shop Address Here\nOpen: 9 AM - 8 PM")
    st.balloons() # Animated indicator for engagement
