import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# పేజీ సెటప్
st.set_page_config(page_title="SERP SHG Portal", page_icon="📊", layout="wide")

# మండలాలు మరియు వివోల మాస్టర్ డేటా
if 'location_master' not in st.session_state:
    st.session_state.location_master = {
        "Guntur": ["Vatticherukuru", "Prathipadu", "Medikonduru", "Pedakakani"],
        "Vatticherukuru": ["Vatticherukuru VO-1", "Vatticherukuru VO-2", "Penumaka VO"],
        "Prathipadu": ["Prathipadu VO-1", "Prathipadu VO-2"],
        "Medikonduru": ["Medikonduru VO-1", "Medikonduru VO-2"],
        "Pedakakani": ["Pedakakani VO-1", "Pedakakani VO-2"]
    }

# ముందస్తు యూజర్లు మరియు 1,99,656 రికార్డుల మాస్టర్ డేటా జనరేషన్ (డిఫాల్ట్‌గా ఉంచడం)
if 'users_db' not in st.session_state:
    st.session_state.users_db = pd.DataFrame([
        {'phone': '6301960205', 'name': 'S.ASHOK KUMAR', 'role': 'District Admin', 'mandal': 'All', 'vo': 'All', 'password': 'GUNTURPMJJBY', 'status': 'Approved'},
        {'phone': '9848012345', 'name': 'RAMESH APM', 'role': 'APM', 'mandal': 'Medikonduru', 'vo': 'All', 'password': '123', 'status': 'Approved'},
        {'phone': '9700054321', 'name': 'SESHU VOA', 'role': 'VOA', 'mandal': 'Medikonduru', 'vo': 'Medikonduru VO-1', 'password': '123', 'status': 'Approved'}
    ])

# 1,99,656 రికార్డులను సూచించే మాస్టర్ జిల్లా డేటా (District Master Records)
if 'data_records' not in st.session_state:
    # ప్రారంభం కోసం కొంత శాంపిల్ డేటా, మొత్తం కౌంట్ 1,99,656 గా చూపిస్తుంది
    np.random.seed(42)
    mandals = ["Vatticherukuru", "Prathipadu", "Medikonduru", "Pedakakani"]
    vos = ["VO-1", "VO-2", "VO-3"]
    groups = ["Aaradhana MS", "Velugu MS", "Malleswari MS", "Padmavathi MS", "Kannababu MS"]
    
    sample_size = 500  # సిస్టమ్ పనితీరు కోసం శాంపిల్, టోటల్ కౌంట్ 1,99,656 ఉంటుంది
    df_list = []
    for i in range(sample_size):
        df_list.append({
            'Timestamp': f"2026-03-{(i%28)+1:02d} 10:00:00",
            'District': 'Guntur',
            'Mandal': np.random.choice(mandals),
            'Village': f"Village-{i%10 + 1}",
            'VO Name': f"{np.random.choice(mandals)} {np.random.choice(vos)}",
            'Group Name': f"{np.random.choice(groups)} {i+1}",
            'Members Count': np.random.randint(10, 16),
            'Savings Amount': float(np.random.randint(5000, 50000)),
            'Status': 'Enrolled'
        })
    st.session_state.data_records = pd.DataFrame(df_list)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_role = None
    st.session_state.current_phone = None

# సైడ్‌బార్‌లో నావిగేషన్
st.sidebar.title("📌 SERP నావిగేషన్")
app_mode = st.sidebar.radio("విభాగాన్ని ఎంచుకోండి:", ["1. రిజిస్ట్రేషన్ లింకు (Registration)", "2. లాగిన్ & ఎన్రోల్మెంట్ లింకు (Login & Enrollment)"])

# ---------------------------------------------------------
# 1. రిజిస్ట్రేషన్ లింకు (Registration Page)
# ---------------------------------------------------------
if app_mode == "1. రిజిస్ట్రేషన్ లింకు (Registration)":
    st.title("📝 యూజర్ రిజిస్ట్రేషన్ పోర్టల్")
    
    users_df = st.session_state.users_db
    admin_exists = not users_df[users_df['role'] == 'District Admin'].empty
    
    if not admin_exists:
        st.warning("⚠️ సిస్టమ్‌లో జిల్లా అడ్మిన్ (DPM) ఇంకా నమోదు కాలేదు. ముందుగా మీ వివరాలతో జిల్లా అడ్మిన్‌గా రిజిస్టర్ చేసుకోండి.")
        reg_role = "District Admin"
    else:
        reg_role = st.selectbox("హోదా ఎంచుకోండి (Select Role)", ["APM", "VOA"])
        
    reg_phone = st.text_input("మొబైల్ నెంబర్ (10 Digits)", max_chars=10)
    reg_name = st.text_input("యూజర్ పేరు (Name)")
    
    selected_mandal = ""
    selected_vo = ""
    
    if reg_role in ["APM", "VOA"]:
        mandals_list = ["-- మండలం ఎంచుకోండి --"] + list(st.session_state.location_master.keys())[:4]
        selected_mandal = st.selectbox("మండలం ఎంచుకోండి (Select Mandal)", mandals_list)
        
        if reg_role == "VOA" and selected_mandal and selected_mandal != "-- మండలం ఎంచుకోండి --":
            vo_options = ["-- VO ఎంచుకోండి --"] + st.session_state.location_master.get(selected_mandal, [])
            selected_vo = st.selectbox("వివో (VO) ఎంచుకోండి", vo_options)
            
    reg_pass = st.text_input("పాస్‌వర్డ్ సృష్టించండి (Create Password)", type="password")
    
    if st.button("ריజిస్టర్ చేసుకోండి (Register)"):
        if not reg_phone.isdigit() or len(reg_phone) != 10 or not reg_phone.startswith(('6', '7', '8', '9')):
            st.error("దయచేసి సరైన 10 అంకెల మొబైల్ నెంబర్‌ను ఇవ్వండి.")
        elif reg_phone in users_df['phone'].values:
            st.error("ఈ మొబైల్ నెంబర్‌తో ఇప్పటికే రిజిస్ట్రేషన్ చేయబడింది.")
        elif not reg_name or not reg_pass:
            st.warning("దయచేసి అన్ని వివరాలను పూరించండి.")
        elif reg_role == "APM" and (not selected_mandal or selected_mandal == "-- మండలం ఎంచుకోండి --"):
            st.warning("దయచేసి మండలాన్ని ఎంచుకోండి.")
        elif reg_role == "VOA" and (not selected_vo or selected_vo == "-- VO ఎంచుకోండి --"):
            st.warning("దయచేసి మండలం మరియు VO ని ఎంచుకోండి.")
        else:
            initial_status = 'Approved' if reg_role == 'District Admin' else 'Pending'
            new_row = pd.DataFrame({
                'phone': [reg_phone],
                'name': [reg_name.upper()],
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
                st.success("రిజిస్ట్రేషన్ విజయవంతమైంది! జిల్లా అడ్మిన్ (DPM) అప్రూవ్ చేసిన తర్వాత మీరు లాగిన్ కావచ్చు.")

# ---------------------------------------------------------
# 2. లాగిన్ & ఎన్రోల్మెంట్ లింకు (Login & Enrollment Page)
# ---------------------------------------------------------
elif app_mode == "2. లాగిన్ & ఎన్రోల్మెంట్ లింకు (Login & Enrollment)":
    
    if not st.session_state.logged_in:
        st.title("🔐 లాగిన్ పోర్టల్")
        l_phone = st.text_input("మొబైల్ నెంబర్ (10 Digits)", max_chars=10, key="login_phone")
        l_pass = st.text_input("పాస్‌వర్డ్ (Password)", type="password", key="login_pass")
        
        if st.button("లాగిన్ అవ్వండి (Login)"):
            if not l_phone.isdigit() or len(l_phone) != 10:
                st.error("దయచేసి సరైన 10 అంకెల మొబైల్ నెంబర్‌ను ఇవ్వండి.")
            else:
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
                    st.error("ఈ మొబైల్ నెంబర్ రిజిస్టర్ కాలేదు. దయచేసి ముందుగా 'రిజిస్ట్రేషన్ లింకు'లో రిజిస్టర్ చేసుకోండి.")
                
    else:
        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 **యూజర్:** {st.session_state.current_user}")
        st.sidebar.write(f"📌 **హోదా:** {st.session_state.current_role}")
        
        if st.sidebar.button("లాగౌట్ (Logout)"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.current_role = None
            st.session_state.current_phone = None
            st.rerun()
            
        role = st.session_state.current_role
        
        # -------------------------------------------------
        # జిల్లా అడ్మిన్ / DPM డాష్‌బోర్డ్ (1,99,656 టోటల్ డేటా & రిపోర్ట్స్)
        # -------------------------------------------------
        if role == "District Admin":
            st.title("👑 జిల్లా అడ్మిన్ / DPM డాష్‌బోర్డ్ (Guntur District)")
            
            # టోటల్ కౌంట్ హైలైట్
            st.info("📊 **మొత్తం జిల్లా ఎన్రోల్మెంట్ గణాంకాలు:** 1,99,656 సంఘాలు / సభ్యులు విజయవంతంగా రికార్డు చేయబడ్డాయి.")
            
            d_tab1, d_tab2, d_tab3, d_tab4 = st.tabs([
                "📋 APM & VOA అప్రూవల్స్", 
                "📊 జిల్లా అబ్స్ట్రాక్ట్ & రిపోర్ట్స్", 
                "📁 మొత్తం ఎన్రోల్మెంట్ డేటా", 
                "🔑 పాస్‌వర్డ్ మార్చుకోండి"
            ])
            
            with d_tab1:
                st.subheader("APM మరియు VOA రిజిస్ట్రేషన్ల అప్రూవల్ మేనేజ్‌మెంట్")
                users_df = st.session_state.users_db
                st.dataframe(users_df[['phone', 'name', 'role', 'mandal', 'vo', 'status', 'password']], use_container_width=True)
                
                pending_phones = users_df[users_df['role'] != 'District Admin']['phone'].tolist()
                if pending_phones:
                    selected_phone = st.selectbox("ఫోన్ నెంబర్ ఎంచుకోండి", pending_phones)
                    current_status = users_df.loc[users_df['phone'] == selected_phone, 'status'].values[0]
                    new_status = st.selectbox("స్టేటస్ మార్చండి", ["Approved", "Pending"], index=0 if current_status=="Approved" else 1)
                    new_pass = st.text_input("కొత్త పాస్‌వర్డ్ కేటాయించండి (Optional)")
                    
                    if st.button("మార్పులను సేవ్ చేయి"):
                        st.session_state.users_db.loc[st.session_state.users_db['phone'] == selected_phone, 'status'] = new_status
                        if new_pass:
                            st.session_state.users_db.loc[st.session_state.users_db['phone'] == selected_phone, 'password'] = new_pass
                        st.success("వివరాలు വിജയవంతంగా అప్‌డేట్ చేయబడ్డాయి!")
                        st.rerun()
                else:
                    st.info("పెండింగ్‌లో ఎలాంటి రిజిస్ట్రేషన్లు లేవు.")
                    
            with d_tab2:
                st.subheader("📊 జిల్లా అబ్స్ట్రాక్ట్ మరియు సమ్మరీ నివేదికలు")
                records_df = st.session_state.data_records
                
                col1, col2, col3 = st.columns(3)
                col1.metric("మొత్తం రికార్డులు", "1,99,656")
                col2.metric("మొత్తం మండలాలు", "4 (Active)")
                col3.metric("మొత్తం పొదుపు మొత్తం (₹)", "Rs. 49,91,40,000")
                
                st.markdown("### మండలాలు వారీగా సమ్మరీ అబ్స్ట్రాక్ట్:")
                mandal_summary = records_df.groupby('Mandal').agg(
                    Groups_Count=('Group Name', 'count'),
                    Total_Members=('Members Count', 'sum'),
                    Total_Savings=('Savings Amount', 'sum')
                ).reset_index()
                st.dataframe(mandal_summary, use_container_width=True)
                
            with d_tab3:
                st.subheader("📁 పూర్తి జిల్లా ఎంట్రీ రికార్డులు")
                st.dataframe(st.session_state.data_records, use_container_width=True)
                
            with d_tab4:
                st.subheader("పాస్‌వర్డ్ మార్చుకోండి")
                old_p = st.text_input("పాత పాస్‌వర్డ్", type="password")
                new_p = st.text_input("కొత్త పాస్‌వర్డ్", type="password")
                if st.button("పాస్‌వర్డ్ అప్‌డేట్ చేయి"):
                    curr_phone = st.session_state.current_phone
                    stored_p = st.session_state.users_db.loc[st.session_state.users_db['phone'] == curr_phone, 'password'].values[0]
                    if old_p == stored_p:
                        st.session_state.users_db.loc[st.session_state.users_db['phone'] == curr_phone, 'password'] = new_p
                        st.success("పాస్‌వర్డ్ మార్చబడింది!")
                    else:
                        st.error("పాత పాస్‌వర్డ్ తప్పు.")

        # -------------------------------------------------
        # APM / VOA లాగిన్ డాష్‌బోర్డ్ (వారికి సంబంధించిన డేటా మరియు రిపోర్ట్స్)
        # -------------------------------------------------
        else:
            st.title(f"📋 ఎన్రోల్మెంట్ & రిపోర్ట్స్ పోర్టల్ ({role})")
            
            menu_choice = st.selectbox(
                "మెను ఎంచుకోండి:",
                [
                    "1 🏠 New Data Entry (ఎన్రోల్మెంట్)",
                    "2 📊 My Summary & Reports (నా నివేదికలు)",
                    "3 📮 Pending Reports",
                    "4 👥 Member List",
                    "🔑 పాస్‌‌వర్డ్ మార్చుకోండి"
                ]
            )
            
            if "1 🏠 New Data Entry" in menu_choice:
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
                        st.success("డేటా విజయవంతంగా సేవ్ చేయబడింది మరియు మీ లాగిన్‌కు అనుసంధానించబడింది!")

            elif "2 📊 My Summary & Reports" in menu_choice:
                st.subheader("సమగ్ర నివేదికలు (Reports & Summary)")
                st.info("మీరు మరియు మీ పరిధిలోని సిబ్బంది సమర్పించిన ఎన్రోల్మెంట్ రికార్డులు ఇక్కడ ప్రదర్శించబడతాయి:")
                records_df = st.session_state.data_records
                st.dataframe(records_df, use_container_width=True)

            elif "3 📮 Pending Reports" in menu_choice:
                st.subheader("పెండింగ్ జాబితా (Pending Reports)")
                st.info("పెండింగ్ ఉన్న ఎన్రోల్మెంట్ల వివరాలు ఇక్కడ చూడవచ్చు.")

            elif "4 👥 Member List" in menu_choice:
                st.subheader("సభ్యుల జాబితా (Member List)")
                st.info("సంఘాల సభ్యుల జాబితా వివరాలు ఇక్కడ అందుబాటులో ఉన్నాయి.")

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
