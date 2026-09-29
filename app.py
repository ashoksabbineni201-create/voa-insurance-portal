import streamlit as st

# పేజ్ ఎంచుకోండి (Select Page) - కేటగిరీల వారీగా క్రమబద్ధీకరించబడింది
st.sidebar.title("పేజ్ ఎంచుకోండి:")

# 1. ఎన్రోల్మెంట్ డ్యాష్‌బోర్డ్
enrolment_dash = st.sidebar.radio(
    "1. ఎన్రోల్మెంట్ డ్యాష్‌బోర్డ్",
    ("ఎన్రోల్మెంట్ డ్యాష్‌బోర్డ్ (Portal)",)
)

# 2. ప్రోగ్రెస్ & డీటెయిల్డ్ రిపోర్ట్స్
progress_reports = st.sidebar.selectbox(
    "2. ప్రోగ్రెస్ & డీటెయిల్డ్ రిపోర్ట్స్",
    (
        "దయచేసి ఎంచుకోండి...",
        "మండల వైజ్ అబ్స్ట్రాక్ట్ & రిపోర్ట్ (Mandal Wise Report)",
        "VO వైజ్ అబ్స్ట్రాక్ట్ & రిపోర్ట్ (Mandal & VO Wise Report)",
        "పెండింగ్ రిపోర్ట్ (Detailed Lists)",
        "SHG & మెంబర్ వైజ్ రిపోర్ట్ (SHG / Member Level Detail)"
    )
)

# 3. బ్యాంక్ రిపోర్ట్స్
bank_reports = st.sidebar.selectbox(
    "3. బ్యాంక్ రిపోర్ట్స్",
    (
        "దయచేసి ఎంచుకోండి...",
        "బ్యాంక్ & బ్రాంచ్ వైజ్ అబ్స్ట్రాక్ట్ (Bank & Branch Wise Report)"
    )
)

# మీరు ఎంచుకున్న ఆప్షన్‌ని బట్టి పేజీని లోడ్ చేసే లాజిక్
if enrolment_dash:
    # ఎన్రోల్మెంట్ డ్యాష్‌బోర్డ్ కోడ్ ఇక్కడ రాయండి
    pass
elif progress_reports != "దయచేసి ఎంచుకోండి...":
    # ప్రోగ్రెస్ రిపోర్ట్స్ కోడ్ ఇక్కడ రాయండి
    st.write(f"Selected Report: {progress_reports}")
elif bank_reports != "దయచేసి ఎంచుకోండి...":
    # బ్యాంక్ రిపోర్ట్స్ కోడ్ ఇక్కడ రాయండి
    st.write(f"Selected Report: {bank_reports}")
