import streamlit as st

st.set_page_config(page_title="Insurance Enrollment Portal", layout="wide")

# Session State ద్వారా ప్రస్తుత పేజీని ట్రాక్ చేయడం
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

if 'selected_mandal' not in st.session_state:
    st.session_state.selected_mandal = None
if 'selected_vo' not in st.session_state:
    st.session_state.selected_vo = None
if 'selected_shg' not in st.session_state:
    st.session_state.selected_shg = None


# ==========================================
# PAGE 1: Filters & Selection Page
# ==========================================
if st.session_state.current_page == 1:
    st.title("📊 ఇన్సూరెన్స్ ఎన్‌రోల్‌మెంట్ పోర్టల్ - ఫిల్టర్లు")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📥 రిపోర్ట్ డౌన్‌లోడ్ & ఆబ్‌స్ట్రాక్ట్")
        if st.button("📥 ఎంట్రీ చేసిన వివరాల రిపోర్ట్ డౌన్‌లోడ్ (CSV)"):
            st.success("రిపోర్ట్ డౌన్‌లోడ్ అవుతోంది...")

        st.markdown("---")
        st.subheader("📍 సెలెక్షన్ వివరాలు")

        # Mandal Selection
        mandal_list = ["-- ఎంచుకోండి --", "Chebrole", "Duggirala", "Guntur", "Kakumanu"]
        mandal = st.selectbox("1. మండలం ఎంచుకోండి:", mandal_list)

        # VO Selection
        vo_list = ["-- ఎంచుకోండి --"]
        if mandal != "-- ఎంచుకోండి --":
            vo_list = ["-- ఎంచుకోండి --", "ADARSHA GRAMIKYA SANGAM", "VIKAS GRAMIKYA SANGAM"]
        vo = st.selectbox("2. VO (Village Organization) పేరు:", vo_list)

        # SHG Selection
        shg_list = ["-- ఎంచుకోండి --"]
        if vo != "-- ఎంచుకోండి --":
            shg_list = ["-- ఎంచుకోండి --", "Ambedkara Mahila Group", "Jyothi Mahila Group"]
        shg = st.selectbox("3. SHG Group ఎంచుకోండి:", shg_list)

        # SHG సెలెక్ట్ చేసుకున్న తర్వాత 2వ పేజీకి వెళ్లే బటన్
        if shg != "-- ఎంచుకోండి --":
            st.markdown("---")
            if st.button("➡️ SHG సభ్యుల జాబితా చూడండి (Next Page)"):
                st.session_state.selected_mandal = mandal
                st.session_state.selected_vo = vo
                st.session_state.selected_shg = shg
                st.session_state.current_page = 2
                st.rerun()

    with col2:
        st.info("💡 దయచేసి ఎడమ వైపు ఉన్న ఫిల్టర్ల నుండి మండలం, VO మరియు SHG ని ఎంచుకోండి. SHG ని ఎంచుకున్న తర్వాత సభ్యుల వివరాలు చూపే 2వ పేజీ ఓపెన్ అవుతుంది.")


# ==========================================
# PAGE 2: Members List Page (SHG Selected)
# ==========================================
elif st.session_state.current_page == 2:
    # వెనక్కి వెళ్లే బటన్
    if st.button("⬅️ బ్యాక్ (ఫిల్టర్ల పేజీకి వెళ్లండి)"):
        st.session_state.current_page = 1
        st.rerun()

    st.markdown("<h4 style='color: #1E88E5;'>🔑 VOA & SHG Insurance Enrollment Portal</h4>", unsafe_allow_html=True)
    st.title("👥 SHG సభ్యుల జాబితా (Dashboard)")

    # ఎంచుకున్న ప్రదేశం యొక్క వివరాలు
    st.info(f"📍 **ఎంచుకున్న వివరాలు:** మండలం: **{st.session_state.selected_mandal}** ➔ VO: **{st.session_state.selected_vo}** ➔ SHG: **{st.session_state.selected_shg}**")

    # ఉదాహరణ సభ్యుల వివరాలు
    members = [
        {"name": "pilli sunitha", "id": "01073405004010106411", "age": 32, "status": "ఎంట్రీ పెండింగ్"},
        {"name": "GERA Prasannakumari", "id": "01073405004010106410", "age": 32, "status": "ఎంట్రీ పెండింగ్"},
        {"name": "medida Anitha", "id": "01073405004010106408", "age": 35, "status": "ఎంట్రీ పెండింగ్"},
        {"name": "pilli Ratnakumari", "id": "01073405004010106409", "age": 38, "status": "ఎంట్రీ పెండింగ్"},
        {"name": "pagadala Ramadevi", "id": "01073405004010106405", "age": 38, "status": "ఎంట్రీ పెండింగ్"},
    ]

    st.subheader(f"📋 {st.session_state.selected_shg} లోని సభ్యుల పేర్లు:")

    for member in members:
        with st.expander(f"✏️ {member['name']} (ID: {member['id']}) | వయస్సు: {member['age']} | Status: {member['status']}"):
            st.write(f"**సభ్యురాలి పేరు:** {member['name']}")
            st.write(f"**ID:** {member['id']}")
            st.write(f"**వయస్సు:** {member['age']}")
            st.write(f"**Status:** {member['status']}")
            # ఇక్కడ ఫారమ్ సబ్మిషన్ లేదా ఎడిట్ వివరాలు ఇవ్వవచ్చు
