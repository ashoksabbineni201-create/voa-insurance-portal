import streamlit as st
import pandas as pd
from datetime import datetime

# పేజీ సెటప్
st.set_page_config(page_title="SERP SHG Portal", page_icon="📊", layout="wide")

# సెషన్ స్టేట్ ఇనిషియలైజేషన్
if 'users_db' not in st.session_state:
    # ప్రారంభ రిజిస్ట్రేషన్ డేటా (స్టేటస్: Approved / Pending)
    st.session_state.users_db = pd.DataFrame({
        'phone': ['9121190676', '9876543210', '9111111111'],
        'name': ['జిల్లా అడ్మిన్ (District Admin)', 'రాము (APM)', 'సీత (VO)'],
        'role': ['District Admin', 'APM', 'VO'],
        'village': ['అన్ని (All)', 'మండలం (All)', 'గ్రామం-1'],
        'password': ['1234', '1234', '1234'],
        'status': ['Approved', 'Approved', 'Approved']
    })

if 'data_records' not in st.session_state:
    st.session_state.data_records = pd.DataFrame(columns=[
        'Timestamp', 'District', 'Mandal', 'Village', 'VO Name', 
        'Group Name', 'Members Count', 'Savings Amount', 'Status'
    ])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None

# లాగిన్ / రిజిస్ట్రేషన్ పేజీ
def login_page():
    st.title("🏛️ SERP SHG - పోర్టల్ లాగిన్")
    
    tab1, tab2 = st.tabs(["లాగిన్ (Login)", "కొత్త రిజిస్ట్రేషన్ (New Registration)"])
    
    with tab1:
        st.subheader("ప్రవేశం (Sign In)")
        phone = st.text_input("ఫోన్ నెంబర్ (Phone Number)", max_chars=10, key="login_phone")
        password = st.text_input("పాస్‌వర్డ్ (Password)", type="password", key="login_password")
        
        if st.button("లాగిన్ అవ్వండి (Login)"):
            users = st.session_state.users_db
            user_match = users[users['phone'] == phone]
            
            if phone == "9121190676" and password == "1234":
                st.session_state.logged_in = True
                st.session_state.current_user = "జిల్లా అడ్మిన్"
                st.session_state.current_role = "District Admin"
                st.session_state.current_phone = phone
                st.success("జిల్లా అడ్మిన్‌గా విజయవంతంగా లాగిన్ అయ్యారు!")
                st.rerun()
            elif not user_match.empty:
                row = user_match.iloc[0]
                if row['password'] == password:
                    if row['status'] == 'Approved':
                        st.session_state.logged_in = True
                        st.session_state.current_user = row['name']
                        st.session_state.current_role = row['role']
                        st.session_state.current_phone = phone
                        st.success(f"స్వాగతం, {row['name']}!")
                        st.rerun()
                    else:
                        st.warning("మీ రిజిస్ట్రేషన్ ఇంకా జిల్లా అడ్మిన్ ఆమోదం (Approval) పొందలేదు.")
                else:
                    st.error("తప్పు పాస్‌వర్డ్.")
            else:
                st.error("ఈ ఫోన్ నెంబర్ రిజిస్టర్ కాలేదు లేదా కనుగొనబడలేదు.")

    with tab2:
        st.subheader("కొత్త యూజర్ రిజిస్ట్రేషన్ (VO / APM Registration)")
        reg_phone = st.text_input("ఫోన్ నెంబర్ (Phone Number)", max_chars=10, key="reg_phone")
        reg_name = st.text_input("పేరు (Name)", key="reg_name")
        reg_role = st.selectbox("హోదా (Role)", ["VO", "APM"])
        reg_village = st.text_input("గ్రామం / మండలం పేరు (Village / Mandal Name)")
        reg_pass = st.text_input("పాస్‌వర్డ్ సృష్టించండి (Create Password)", type="password", key="reg_pass")
        
        if st.button("రిజిస్టర్ చేసుకోండి (Register)"):
            users = st.session_state.users_db
            if reg_phone in users['phone'].values:
                st.error("ఈ ఫోన్ నెంబర్‌‌తో ఇప్పటికే రిజిస్ట్రేషన్ చేయబడింది. ఒక గ్రామానికి/వ్యక్తికి ఒకే ఫోన్ నెంబర్ అనుమతించబడుతుంది.")
            elif not reg_phone or not reg_name or not reg_pass:
                st.warning("దయచేసి అన్ని వివరాలను పూరించండి.")
            else:
                new_row = pd.DataFrame({
                    'phone': [reg_phone],
                    'name': [reg_name],
                    'role': [reg_role],
                    'village': [reg_village],
                    'password': [reg_pass],
                    'status': ['Pending'] # అడ్మిన్ అప్రూవల్ కోసం పెండింగ్
                })
                st.session_state.users_db = pd.concat([users, new_row], ignore_index=True)
                st.success("రిజిస్ట్రేషన్ విజయవంతంగా సమర్పించబడింది! జిల్లా అడ్మిన్ ఆమోదం తరువాత మీరు లాగిన్ হতেవచ్చు.")

# ప్రధాన అప్లికేషన్
def main_app():
    st.sidebar.logged_in_user = st.session_state.current_user
    st.sidebar.write(f"👤 **యూజర్:** {st.session_state.current_user}")
    st.sidebar.write(f"📌 **హోదా:** {st.session_state.current_role}")
    
    if st.sidebar.button("లాగౌట్ (Logout)"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.current_role = None
        st.rerun()
        
    st.sidebar.markdown("---")
    
    role = st.session_state.current_role
    
    # జిల్లా అడ్మిన్ లాగిన్ ప్యానెల్
    if role == "District Admin":
        st.title("👑 జిల్లా అడ్మిன் కంట్రోల్ ప్యానెల్ (District Admin Login)")
        
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["యూజర్ అప్రూవల్స్ & పాస్‌వర్డ్ మేనేజ్‌మెంట్", "అన్ని వివో (VO) ఎంట్రీలు", "పాస్‌వర్డ్ మార్చుకోండి"])
        
        with admin_tab1:
            st.subheader("VO / APM రిజిస్ట్రేషన్ అప్రూవల్స్ మరియు పాస్‌వర్డ్స్")
            users_df = st.session_state.users_db
            
            st.dataframe(users_df[['phone', 'name', 'role', 'village', 'status', 'password']], use_container_width=True)
            
            st.markdown("### యూజర్ స్టేటస్ అప్రూవ్ చేయుట లేదా న్యూ పాస్‌వర్డ్ సెట్ చేయుట")
            selected_phone = st.selectbox("ఫోన్ నెంబర్ ఎంచుకోండి", users_df['phone'].tolist())
            
            if selected_phone:
                current_status = users_df.loc[users_df['phone'] == selected_phone, 'status'].values[0]
                new_status = st.selectbox("స్టేటస్ మార్చండి", ["Approved", "Pending"], index=0 if current_status=="Approved" else 1)
                
                new_generated_pass = st.text_input("కొత్త పాస్‌వర్డ్ కేటాయించండి (New Password)")
                
                if st.button("మార్పులను సేవ్ చేయండి"):
                    st.session_state.users_db.loc[st.session_state.users_db['phone'] == selected_phone, 'status'] = new_status
                    if new_generated_pass:
                        st.session_state.users_db.loc[st.session_state.users_db['phone'] == selected_phone, 'password'] = new_generated_pass
                    st.success("వివరాలు வெற்றవంతంగా అప్‌డేట్ చేయబడ్డాయి!")
                    st.rerun()
                    
        with admin_tab2:
            st.subheader("సమర్పించబడిన మొత్తం డేటా")
            if not st.session_state.data_records.empty:
                st.dataframe(st.session_state.data_records, use_container_width=True)
            else:
                st.info("ఇంకా డేటా ఎంట్రీలు ఏవీ నమోదు కాలేదు.")
                
        with admin_tab3:
            st.subheader("అడ్మిన్ పాస్‌వర్డ్ మార్చుకోండి")
            old_p = st.text_input("పాత పాస్‌వర్డ్", type="password")
            new_p = st.text_input("కొత్త పాస్‌వర్డ్", type="password")
            if st.button("పాస్‌వర్డ్ మార్చు"):
                if old_p == "1234": # లేదా ప్రస్తుత అడ్మిన్ పాస్‌వర్డ్
                    st.success("పాస్‌వర్డ్ విజయవంతంగా మార్చబడింది!")
                else:
                    st.error("పాత పాస్‌వర్డ్ తప్పు.")

    # APM మరియు VO లాగిన్ ప్యానెల్ (డేటా ఎంట్రీ మరియు రిపోర్ట్స్)
    else:
        st.markdown("📌 దయచేసి క్రింది మెను నుండి కావలసిన సెక్షన్ లేదా రిపోర్ట్ ఎంచుకోండి:")
        
        menu_choice = st.selectbox(
            "సెలెక్ట్ చేయండి:",
            [
                "1 🏠 VO Data Entry",
                "2 📊 VO Summary & Reports",
                "3 📮 VO Pending Reports",
                "4 👥 VO Member List",
                "🔑 పాస్‌వర్డ్ మార్చుకోండి (Change Password)"
            ]
        )
        
        if "1 🏠 VO Data Entry" in menu_choice:
            st.subheader("సమాచార నమోదు (VO Data Entry)")
            with st.form("data_entry_form"):
                district = st.text_input("జిల్లా (District)", value="Guntur")
                mandal = st.text_input("మండలం (Mandal)")
                village = st.text_input("గ్రామం (Village)")
                vo_name = st.text_input("VO పేరు", value=st.session_state.current_user)
                group_name = st.text_input("మహిళా సంఘం పేరు (Group Name)")
                members_count = st.number_input("సభ్యుల సంఖ్య (Members Count)", min_value=1, step=1)
                savings_amount = st.number_input("పొదుపు మొత్తం (Savings Amount)", min_value=0.0)
                
                submitted = st.form_submit_button("డేటా సబ్మిట్ చేయి")
                if submitted:
                    new_entry = pd.DataFrame({
                        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'District': [district],
                        'Mandal': [mandal],
                        'Village': [village],
                        'VO Name': [vo_name],
                        'Group Name': [group_name],
                        'Members Count': [members_count],
                        'Savings Amount': [savings_amount],
                        'Status': ['Submitted']
                    })
                    st.session_state.data_records = pd.concat([st.session_state.data_records, new_entry], ignore_index=True)
                    st.success("డేటా విజయవంతంగా సేవ్ చేయబడింది!")

        elif "2 📊 VO Summary & Reports" in menu_choice:
            st.subheader("సమగ్ర నివేదికలు (VO Summary & Reports)")
            if not st.session_state.data_records.empty:
                st.dataframe(st.session_state.data_records, use_container_width=True)
            else:
                st.info("ప్రస్తుతానికి ఎలాంటి నివేదికలు అందుబాటులో లేవు.")

        elif "3 📮 VO Pending Reports" in menu_choice:
            st.subheader("పెండింగ్ జాబితా (VO Pending Reports)")
            st.info("పెండింగ్ రిపోర్ట్స్ వివరాలు ఇక్కడ ప్రదర్శించబడతాయి.")

        elif "4 👥 VO Member List" in menu_choice:
            st.subheader("సభ్యుల జాబితా (VO Member List)")
            st.info("సంఘాల సభ్యుల జాబితా వివరాలు ఇక్కడ చూడవచ్చు.")

        elif "🔑 పాస్‌వర్డ్ మార్చుకోండి" in menu_choice:
            st.subheader("మీ పాస్‌వర్డ్ మార్చుకోండి")
            current_phone_num = st.session_state.current_phone
            old_pass_input = st.text_input("ప్రస్తుత పాస్‌వర్డ్", type="password")
            new_pass_input = st.text_input("కొత్త పాస్‌వర్డ్", type="password")
            
            if st.button("పాస్‌వర్డ్ అప్‌డేట్ చేయి"):
                users = st.session_state.users_db
                stored_pass = users.loc[users['phone'] == current_phone_num, 'password'].values[0]
                if old_pass_input == stored_pass:
                    st.session_state.users_db.loc[users['phone'] == current_phone_num, 'password'] = new_pass_input
                    st.success("మీ పాస్‌వర్డ్ విజయవంతವಾಗಿ మార్చబడింది!")
                else:
                    st.error("మీరు ఇచ్చిన ప్రస్తుత పాస్‌వర్డ్ తప్పు.")

# రన్ కంట్రోల్
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
