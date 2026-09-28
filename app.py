import streamlit as st
import pandas as pd

# ఉదాహరణ డేటా (Example Data)
data = {
    'Mandal': ['Chebrole', 'Chebrole', 'Duggirala', 'Duggirala', 'Guntur'],
    'VO_Name': ['VO 1', 'VO 2', 'VO A', 'VO B', 'VO X'],
    'Total_Members': [8000, 8367, 7000, 7219, 7603],
    'Updated_Members': [0, 0, 0, 0, 0]
}
df = pd.DataFrame(data)

st.title("📊 మండల & VOల వారీగా ఆబ్‌స్ట్రాక్ట్ రిపోర్ట్")

# 1. Mandal Wise Abstract Summary Table
mandal_summary = df.groupby('Mandal').agg(
    Total_Members=('Total_Members', 'sum'),
    Updated_Members=('Updated_Members', 'sum')
).reset_index()

st.subheader("🏢 మండలాల వారీగా వివరాలు (Mandal Summary)")
st.caption("క్రింది పట్టికలో మండలాన్ని ఎంచుకోండి:")

# Selectbox లేదా Table Selection ద్వారా Drill-down
selected_mandal = st.selectbox("మండలాన్ని ఎంచుకోండి (Select Mandal to Drill-Down):", ["-- ఎంచుకోండి --"] + list(mandal_summary['Mandal'].unique()))

# 2. Drill-Down VO Wise Table
if selected_mandal != "-- ఎంచుకోండి --":
    st.markdown("---")
    st.subheader(f"🔍 {selected_mandal} మండలం - VOల వారీగా డ్రిల్ డౌన్ రిపోర్ట్")
    
    # Filter VO Data for Selected Mandal
    vo_filtered = df[df['Mandal'] == selected_mandal]
    
    st.dataframe(vo_filtered[['VO_Name', 'Total_Members', 'Updated_Members']], use_container_width=True)
