import streamlit as st
import pandas as pd
from datetime import datetime

# పేజీ సెటప్
st.set_page_config(page_title="SERP SHG Portal", page_icon="📊", layout="wide")

# మండలాలు మరియు వివోల మాస్టర్ డేటా (డ్రిల్-డౌన్ కోసం)
if 'location_master' not in st.session_state:
    st.session_state.location_master = {
        "Guntur": ["Vatticherukuru", "Prathipadu", "Medikonduru", "Pedakakani"],
        "Vatticherukuru": ["Vatticherukuru VO-1", "Vatticherukuru VO-2", "Penumaka VO"],
        "Prathipadu": ["Prathipadu VO-1", "Prathipadu VO-2"],
        "Medikonduru": ["Medikonduru VO-1", "Medikonduru VO-2"],
        "Pedakakani": ["Pedakakani VO-1", "Pedakakani VO-2"]
    }

# సెషన్ స్టేట్ ఇనిషియలైజేషన్
if 'users_db' not in st.session_state:
    st.session_state.users_db = pd.DataFrame(columns=[
        'phone', 'name', 'role', 'mandal', 'vo', 'password', 'status'
    ])

if 'data_records' not in st.session_state:
    st.session_state.data_records = pd.DataFrame(columns=[
        'Timestamp', 'District', 'Mandal', 'Village', 'VO Name', 
        'Group Name', 'Members Count', 'Savings Amount', 'Status'
    ])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None

# సైడ్‌బార్‌లో రెండు ప్రధాన లింకులు / సెక్షన్‌లు
st.sidebar.title("📌 SERP నావిగేషన్")
app_mode = st.sidebar.radio("విభాగాన్ని ఎంచుకోండి:", ["1. రిజిస్ట్రేషన్ లింకు (Registration)", "2. లాగిన్ & ఎన్రోల్మెంట్ లింకు (Login & Enrollment)"])

# ---------------------------------------------------------
# 1. రిజిస్ట్రేషన్ లింకు పేజీ
# ---------------------------------------------------------
if app_mode == "1. రిజిస్ట్రేషన్ లింకు (Registration)":
    st.title("📝 యూజర్ రిజిస్ట్రేషన్ పోర్టల్")
    
    users_df = st.session_state.users_db
    admin_exists = not users_df[users_df['role'] == 'District Admin'].empty
    
    if not admin_exists:
        st.warning("⚠️ సిస్టమ్‌లో జిల్లా అడ్మిన్ (DPM) ఇంకా నమోదు కాలేదు. దయచేసి ముందుగా మీ వివరాలతో జిల్లా అడ్మిన్‌గా రిజిస్టర్ చేసుకోండి.")
        reg_role = "District Admin"
    else:
        reg_role = st.selectbox("హోదా ఎంచుకోండి (Select Role)", ["APM", "VOA"])
        
    reg_phone = st.text_input("ఫోన్ నెంబర్ (Phone Number)", max_chars=10)
    reg_name = st.text_input("పేరు (Name)")
    
    selected_mandal = ""
    selected_vo = ""
    
    if reg_role in ["APM", "VOA"]:
        mandals_list = ["-- మండలం ఎంచుకోండి --"] + list(st.session_state.location_master.keys())[:4]
        selected_mandal = st.selectbox("మండలం ఎంచుకోండి (Select Mandal)", mandals_list)
        
        if reg_role == "VOA" and selected_mandal and selected_mandal != "-- మండలం ఎంచుకోండి --":
            vo_options = ["-- VO ఎంచుకోండి --"] + st.session_state.location_master.get(selected_mandal, [])
            selected_vo = st.selectbox("వివో (VO) ఎంచుకోండి", vo_options)
            
    reg_pass = st.text_input("పాస్‌వర్డ్ సృష్టించండి (Create Password)", type="password")
    
    if st.button("రిజిస్టర్ చేసుకోండి (Register)"):
        if reg_phone in users_df['phone'].values:
            st.error("ఈ ఫోన్ నెంబర్‌తో ఇప్పటికే రిజిస్ట్రేషన్ చేయబడింది. ఒక వ్యక్తికి/గ్రామానికి ఒకే ఫోన్ నెంబర్ అనుమతించబడుతుంది.")
        elif not reg_phone or not reg_name or not reg_pass:
            st.warning("దయచేసి అన్ని వివరాలను పూరించండి.")
        elif reg_role == "APM" and (not selected_mandal or selected_mandal == "-- మండలం ఎంచుకోండి --"):
            st.warning("దయచేసి మండలాన్ని ఎంచుకోండి.")
        elif reg_role == "VOA" and (not selected_vo or selected_vo == "-- VO ఎంచుకోండి --"):
            st.warning("దయచేసి మండలం మరియు వివో (VO) రెండూ ఎంచుకోండి.")
        else:
            initial_status = 'Approved' if reg_role == 'District Admin' else 'Pending'
            new_row = pd.DataFrame({
                'phone': [reg_phone],
                'name': [reg_name],
                'role': [reg_role],
                'mandal': [selected_mandal if reg_role != 'District Admin' else 'All'],
                'vo': [selected_vo if reg_role == 'VOA' else 'All'],
                'password': [reg_pass],
                'status': [initial_status]
            })
            st.session_state.users_db = pd.concat([users_df, new_row], ignore_index=True)
            if reg_role == 'District Admin':
                st.success("జిల్లా అడ్మిన్ రిజిస్ట్రేషన్ విజయవంతమైంది! ఇప్పుడు 'లాగిన్ & ఎన్రోల్మెంట్ లింకు'లోకి వెళ్ళి లాగిన్ అవ్వండి.")
            else:
                st.success("రిజిస్ట్రేషన్ విజయవంతంగా సమర్పించబడింది! జిల్లా అడ్మిన్ (DPM) అప్రూవ్ చేసిన తర్వాత మీరు లాగిన్ కావచ్చు.")

# ---------------------------------------------------------
# 2. లాగిన్ & ఎన్రోల్మెంట్ లింకు పేజీ
# ---------------------------------------------------------
elif app_mode == "2. లాగిన్ & ఎన్రోల్మెంట్ లింకు (Login & Enrollment)":
    
    # ఒకవేళ లాగిన్ కాకపోతే లాగిన్ స్క్రీన్ చూపించు
    if not st.session_state.logged_in:
        st.title("🔐 లాగిన్ పోర్టల్ (Login)")
        l_phone = st.text_input("ఫోన్ నెంబర్ (Phone Number)", max_chars=10, key="login_phone")
        l_pass = st.text_input("పాస్‌వర్డ్ (Password)", type="password", key="login_pass")
        
        if st.button("లాగిన్ అవ్వండి (Login)"):
            users_df = st.session_state.users_db
            user_match = users_df[users_df['phone'] == l_phone]
            
            if not user_match.empty:
                row = user_match.iloc[0]
                if row['password'] == l_pass:
                    if row['status'] == 'Approved' or row['role'] == 'District Admin':
                        st.session_state.logged_in = True
                        st.session_state.current_user = row['name']
                        st.session_state.current_role = row['role']
                        st.session_state.current_phone = l_phone
                        st.success(f"స్వాగతం, {row['name']}!")
                        st.rerun()
                    else:
                        st.warning("మీ రిజిస్ట్రేషన్ ఇంకా జిల్లా అడ్మిన్ అప్రూవల్ (Approval) కోసం పెండింగ్‌లో ఉంది.")
                else:
                    st.error("తప్పు పాస్‌వర్డ్.")
            else:
                st.error("ఈ ఫోన్ నెంబర్ రిజిస్టర్ కాలేదు. దయచేసి ముందుగా 'రిజిస్ట్రేషన్ లింకు'లో రిజిస్టర్ చేసుకోండి.")
                
    # లాగిన్ అయిన తర్వాత కనిపించే ఎన్రోల్మెంట్ & అడ్మిన్ డాష్‌బోర్డ్
    else:
        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 **యూజర్:** {st.session_state.current_user}")
        st.sidebar.write(f"📌 **హోదా:** {st.session_state.current_role}")
        
        if st.sidebar.button("లాగౌట్ (Logout)"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.current_role = None
            st.rerun()
            
        role = st.session_state.current_role
        
        # జిల్లా అడ్మిన్ / DPM ప్యానెల్
        if role == "District Admin":
            st.title("👑 జిల్లా అడ్మిన్ / DPM కంట్రోల్ ప్యానెల్")
            
            admin_tab1, admin_tab2, admin_tab3 = st.tabs(["APM & VOA అప్రూవల్స్", "అన్ని ఎంట్రీలు", "పాస్‌‌వర్డ్ మార్చుకోండి"])
            
            with admin_tab1:
                st.subheader("APM మరియు VOA రిజిస్ట్రేషన్ అప్రూవల్స్ మరియు మేనేజ్‌మెంట్")
                users_df = st.session_state.users_db
                st.dataframe(users_df[['phone', 'name', 'role', 'mandal', 'vo', 'status', 'password']], use_container_width=True)
                
                pending_phones = users_df[users_df['role'] != 'District Admin']['phone'].tolist()
                if pending_phones:
                    selected_phone = st.selectbox("ఫోన్ నెంబర్ ఎంచుకోండి", pending_phones)
                    current_status = users_df.loc[users_df['phone'] == selected_phone, 'status'].values[0]
                    new_status = st.selectbox("స్టేటస్ మార్చండి", ["Approved", "Pending"], index=0 if current_status=="Approved" else 1)
                    new_pass = st.text_input("కొత్త పాస్‌వర్డ్ కేటాయించండి (Optional)")
                    
                    if st.button("మార్పులను సేవ్ చేయండి"):
                        st.session_state.users_db.loc[st.session_state.users_db['phone'] == selected_phone, 'status'] = new_status
                        if new_pass:
                            st.session_state.users_db.loc[st.session_state.users_db['phone'] == selected_phone, 'password'] = new_pass
                        st.success("వివరాలు വിജയవంతంగా అప్‌డేట్ చేయబడ్డాయి!")
                        st.rerun()
                else:
                    st.info("పెండింగ్‌లో ఎలాంటి రిజిస్ట్రేషన్లు లేవు.")
                    
            with admin_tab2:
                st.subheader("సమర్పించబడిన మొత్తం డేటా (Enrollment Records)")
                if not st.session_state.data_records.empty:
                    st.dataframe(st.session_state.data_records, use_container_width=True)
                else:
                    st.info("ఇంకా డేటా ఎంట్రీలు ఏవీ నమోదు కాలేదు.")
                    
            with admin_tab3:
                st.subheader("పాస్‌వర్డ్ మార్చుకోండి")
                old_p = st.text_input("పాత పాస్‌వర్డ్", type="password")
                new_p = st.text_input("కొత్త పాస్‌వర్డ్", type="password")
                if st.button("పాస్‌వర్డ్ మార్చు"):
                    curr_phone = st.session_state.current_phone
                    stored_p = st.session_state.users_db.loc[st.session_state.users_db['phone'] == curr_phone, 'password'].values[0]
                    if old_p == stored_p:
                        st.session_state.users_db.loc[st.session_state.users_db['phone'] == curr_phone, 'password'] = new_p
                        st.success("పాస్‌వర్డ్ మార్చబడింది!")
                    else:
                        st.error("పాత పాస్‌వర్డ్ తప్పు.")

        # APM మరియు VOA ఎన్రోల్మెంట్ / డేటా ఎంట్రీ ప్యానెల్
        else:
            st.title("📋 ఎన్రోల్మెంట్ & డేటా ఎంట్రీ పోర్టల్")
            menu_choice = st.selectbox(
                "మెను ఎంచుకోండి:",
                [
                    "1 🏠 VO Data Entry",
                    "2 📊 VO Summary & Reports",
                    "3 📮 VO Pending Reports",
                    "4 👥 VO Member List",
                    "🔑 పాస్‌వర్డ్ మార్చుకోండి (Change Password)"
                ]
            )
            
            if "1 🏠 VO Data Entry" in menu_choice:
                st.subheader("సమచార నమోదు (VO Data Entry)")
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
                curr_phone = st.session_state.current_phone
                old_pass_input = st.text_input("ప్రస్తుత పాస్‌వర్డ్", type="password")
                new_pass_input = st.text_input("కొత్త పాస్‌వర్డ్", type="password")
                
                if st.button("పాస్‌వర్డ్ అప్‌డేట్ చేయి"):
                    users = st.session_state.users_db
                    stored_pass = users.loc[users['phone'] == curr_phone, 'password'].values[0]
                    if old_pass_input == stored_pass:
                        st.session_state.users_db.loc[users['phone'] == curr_phone, 'password'] = new_pass_input
                        st.success("మీ పాస్‌వర్డ్ విజయవంతವಾಗಿ మార్చబడింది!")
                    else:
                        st.error("మీరు ఇచ్చిన ప్రస్తుత పాస్‌వర్డ్ తప్పు.")
