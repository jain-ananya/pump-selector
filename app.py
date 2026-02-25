import streamlit as st
import pandas as pd
import time

# 1. Page Configuration & Professional Theme
st.set_page_config(page_title="CRI Pump Selector", layout="wide", page_icon="🚀")

# Enhanced Custom CSS for Cards and Hover Effects
st.markdown("""
    <style>
    .pump-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        border: 1px solid #eaeaea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .pump-card:hover {
        transform: translateY(-5px);
        border-color: #e63946;
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    .top-badge {
        background-color: #e63946;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .card-title {
        color: #1d3557;
        margin-top: 10px;
        font-size: 22px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Optimized Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('clean_pumps.csv')
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("Missing 'clean_pumps.csv' file.")
        st.stop()

df = load_data()

# 3. Enhanced Sidebar
with st.sidebar:
    st.image("https://www.crigroups.com/wp-content/uploads/2018/05/logo.png", use_container_width=True)
    st.divider()
    
    st.header("🎯 Pump Finder")
    
    # SINGLE DROP DOWN for Category (as requested)
    pump_types = df['Pump Type'].unique().tolist()
    selected_type = st.selectbox(
        "Choose Pump Category", 
        options=pump_types,
        help="Select the general type of pump you are looking for."
    )

    st.subheader("📏 Dimensions")
    depth = st.number_input("Borewell Depth (meters)", min_value=0, value=40)
    tank_height = st.number_input("Tank Height (meters)", min_value=0, value=10)
    
    st.divider()
    
    # BETTER SHOP LOCATION (Popover style)
    st.subheader("📍 Visit Our Store")
    with st.popover("Show Store Details", use_container_width=True):
        st.markdown("""
        **Mahavir Pumps & Hardware**
        M G Road Raipur, Raipur-Chhattisgarh
        
        📞 **7041450979**
        ⏰ **9 AM - 8 PM** (Mon-Sat)
        """)
        st.link_button("Open in Google Maps", "https://www.google.com/maps/search/Mahavir+Pumps+Hardware+Raipur")

    # CONTACT BUTTONS
    st.subheader("📞 Quick Support")
    st.link_button("Chat on WhatsApp", "https://wa.me/919500401115", use_container_width=True)
    st.write("Toll Free: `1800 121 1243`")

# 4. Main App Logic
total_head = (depth + tank_height) * 1.10

st.title("🚀 CRI Pump Smart Selector")
st.write(f"Showing best matches for **{selected_type}** at **{total_head:.1f}m** total head.")

# Progress indicator
with st.status("Analyzing technical data...", expanded=False) as status:
    time.sleep(0.8)
    # Filtering Logic
    recommendations = df[
        (df['Pump Type'] == selected_type) & 
        (df['Max Head (m)'] >= total_head)
    ].sort_values(by=['HP', 'Max Head (m)'])
    status.update(label="Analysis Complete!", state="complete", expanded=False)

# 5. Top 3 Results (Card View)
if not recommendations.empty:
    st.subheader("⭐ Recommended Top Matches")
    top_3 = recommendations.head(3)
    
    cols = st.columns(3)
    for i, (index, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div class="pump-card">
                    <span class="top-badge">Choice #{i+1}</span>
                    <div class="card-title">{row['Series']}</div>
                    <p style="color: #457b9d; font-weight: 600;">Model: {row['Model']}</p>
                    <hr style="margin: 15px 0; border: 0; border-top: 1px solid #eee;">
                    <p>⚡ <b>Power:</b> {row['HP']} HP</p>
                    <p>🏗️ <b>Max Head:</b> {row['Max Head (m)']}m</p>
                    <p>🚰 <b>Outlet:</b> {row['Outlet Size (mm)']}mm</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander(f"More Specs for {row['Model']}"):
                st.write(f"**Applications:** {row['Applications']}")
                st.write(f"**Power (kW):** {row['kW']}")

    # 6. Comparison Table
    st.divider()
    st.subheader("🔍 Side-by-Side Comparison")
    compare_models = st.multiselect(
        "Select specific models to compare details:", 
        options=recommendations['Model'].tolist(),
        default=top_3['Model'].tolist()
    )
    
    if compare_models:
        compare_df = df[df['Model'].isin(compare_models)].set_index('Model')
        st.dataframe(
            compare_df[['Series', 'HP', 'Max Head (m)', 'Outlet Size (mm)', 'Applications']],
            use_container_width=True
        )

else:
    st.warning(f"No {selected_type} pumps found for a {total_head:.1f}m depth. Try selecting a different category or reducing the depth requirement.")
    st.info("💡 Tip: Submersible pumps typically handle greater depths than Jet pumps.")
