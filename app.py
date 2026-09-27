import streamlit as st
from datetime import date

st.set_page_config(page_title="VOA Insurance Enrollment Portal", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 24px; font-weight: bold; color: #1f77b4; text-align: center; }
    .sub-title { font-size: 18px; font-weight: bold; color: #333333; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🔑 VOA & SHG Insurance Enrollment Portal</p>', unsafe_allow_html=True)
st.write("---")

st.sidebar.header("📂 నావిగేషన్")
mandal = st.sidebar.selectbox("మండలం ఎంచుకోండి", ["Guntur Urban", "Prathipadu", "Vatticherukuru", "Tadikonda"])
vo_name = st.sidebar.text_input("VO (Village Organization) పేరు", "Sri Lakshmi VO")
shg_name = st.sidebar.selectbox("SHG గ్రూప్ ఎంచుకోండి", ["SHG - 01 (Velugu)", "SHG - 02 (Indira)", "SHG - 03 (Dwakra)"])

st.sidebar.write("---")
st.sidebar.info(f"📍 ఎంచుకున్న లొకేషన్:\n**{mandal} ➔ {vo_name} ➔ {shg_name}**")

# సభ్యుల డేటా
if 'members_data' not in st.session_state:
    st.session_state['members_data'] = [
        {"ID": 1, "Name": "సుబ్బమ్మ", "Age": 42, 
         "PMJJBY_Status": "Done", "PMJJBY_AppDate": "2026-05-10", "PMJJBY_EnrolDate": "2026-05-15",
         "PMSBY_Status": "Done", "PMSBY_AppDate": "2026-05-10", "PMSBY_EnrolDate": "2026-05-15",
         "BankName": "SBI", "Branch": "Guntur Main", "AccNo": "30123456789"},
        
        {"ID": 2, "Name": "నాగమణి", "Age": 55, 
         "PMJJBY_Status": "N/A", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Pending at Bank", "PMSBY_AppDate": "2026-09-01", "PMSBY_EnrolDate": "-",
         "BankName": "Andhra Bank", "Branch": "Prathipadu", "AccNo": "40234567891"},
        
        {"ID": 3, "Name": "లక్ష్మి", "Age": 62, 
         "PMJJBY_Status": "N/A", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Pending at VOA", "PMSBY_AppDate": "-", "PMSBY_EnrolDate": "-",
         "BankName": "Union Bank", "Branch": "Vatticherukuru", "AccNo": "50345678912"},
        
        {"ID": 4, "Name": "మంగమ్మ", "Age": 72, 
         "PMJJBY_Status": "N/A", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "N/A", "PMSBY_AppDate": "-", "PMSBY_EnrolDate": "-",
         "BankName": "-", "Branch": "-", "AccNo": "-"},
        
        {"ID": 5, "Name": "రాధ", "Age": 35, 
         "PMJJBY_Status": "Pending at Bank", "PMJJBY_AppDate": "2026-09-10", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Pending at VOA", "PMSBY_AppDate": "-", "PMSBY_EnrolDate": "-",
         "BankName": "SBI", "Branch": "Tadikonda", "AccNo": "30456789123"},
        
        {"ID": 6, "Name": "సీత", "Age": 48, 
         "PMJJBY_Status": "Done", "PMJJBY_AppDate": "2026-04-01", "PMJJBY_EnrolDate": "2026-04-05",
         "PMSBY_Status": "Done", "PMSBY_AppDate": "2026-04-01", "PMSBY_EnrolDate": "2026-04-05",
         "BankName": "IOB", "Branch": "Guntur Branch", "AccNo": "60567891234"},
        
        {"ID": 7, "Name": "పార్వతి", "Age": 60, 
         "PMJJBY_Status": "N/A", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Done", "PMSBY_AppDate": "2026-06-12", "PMSBY_EnrolDate": "2026-06-18",
         "BankName": "Grameena Bank", "Branch": "Prathipadu", "AccNo": "70678912345"},
        
        {"ID": 8, "Name": "దుర్గ", "Age": 38, 
         "PMJJBY_Status": "Pending at VOA", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Pending at VOA", "PMSBY_AppDate": "-", "PMSBY_EnrolDate": "-",
         "BankName": "Canara Bank", "Branch": "Guntur Main", "AccNo": "80789123456"},
        
        {"ID": 9, "Name": "భవాని", "Age": 52, 
         "PMJJBY_Status": "N/A", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Pending at Bank", "PMSBY_AppDate": "2026-09-20", "PMSBY_EnrolDate": "-",
         "BankName": "SBI", "Branch": "Vatticherukuru", "AccNo": "30891234567"},
        
        {"ID": 10, "Name": "కమల", "Age": 68, 
         "PMJJBY_Status": "N/A", "PMJJBY_AppDate": "-", "PMJJBY_EnrolDate": "-",
         "PMSBY_Status": "Pending at VOA", "PMSBY_AppDate": "-", "PMSBY_EnrolDate": "-",
         "BankName": "Union Bank", "Branch": "Tadikonda", "AccNo": "50912345678"}
    ]

# పెండింగ్ గణనలు
bank_pending_count = {}
voa_pending_count = 0
for m in st.session_state['members_data']:
    b_name = m['BankName']
    for scheme in ['PMJJBY_Status', 'PMSBY_Status']:
        status = m[scheme]
        if status == "Pending at Bank":
            bank_pending_count[b_name] = bank_pending_count.get(b_name, 0) + 1
        elif status == "Pending at VOA":
            voa_pending_count += 1

st.markdown('<p class="sub-title">📊 పెండింగ్ సమ్మరీ రిపోర్ట్ (VOA & Bank Summary)</p>', unsafe_allow_html=True)
col_s1, col_s2 = st.columns(2)
with col_s1:
    st.info(f"📌 **VOA దగ్గర పెండింగ్ ఉన్నవి:** `{voa_pending_count}` అప్లికేషన్లు")
with col_s2:
    bank_summary_str = " | ".join([f"**{bank}**: {count}" for bank, count in bank_pending_count.items()])
    st.warning(f"🏦 **బ్యాంక్ నందు పెండింగ్ ఉన్నవి:** {bank_summary_str if bank_summary_str else 'ఏమీ లేవు'}")

st.write("---")

st.markdown('<p class="sub-title">👥 SHG సభ్యుల జాబితా (Dashboard)</p>', unsafe_allow_html=True)

for m in st.session_state['members_data']:
    st.write(f"🆔 **ID: {m['ID']}** | 👤 **{m['Name']}** (వయస్సు: {m['Age']}) | PMJJBY: `{m['PMJJBY_Status']}` | PMSBY: `{m['PMSBY_Status']}`")

st.write("---")

st.markdown('<p class="sub-title">⚙️ సభ్యురాలి ఎన్‌రోల్‌మెంట్ & బ్యాంక్ వివరాల అప్‌డేట్</p>', unsafe_allow_html=True)

member_options = [f"ID: {m['ID']} - {m['Name']}" for m in st.session_state['members_data']]
selected_member_str = st.selectbox("సభ్యురాలిని ఎంచుకోండి:", member_options)
selected_id = int(selected_member_str.split(" - ")[0].replace("ID: ", ""))
member = next(m for m in st.session_state['members_data'] if m['ID'] == selected_id)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 👤 సభ్యురాలు: **{member['Name']}** (ID: {member['ID']})")
    
    current_age = st.number_input("వయస్సు (Age) సరిచూడండి / మార్చండి:", value=int(member['Age']), min_value=18, max_value=100)
    member['Age'] = current_age

    st.write(f"🔹 **PMJJBY స్థితి:** `{member['PMJJBY_Status']}` (App Date: {member['PMJJBY_AppDate']} | Enrol Date: {member['PMJJBY_EnrolDate']})")
    st.write(f"🔹 **PMSBY స్థితి:** `{member['PMSBY_Status']}` (App Date: {member['PMSBY_AppDate']} | Enrol Date: {member['PMSBY_EnrolDate']})")

with col2:
    st.markdown("### 📋 ఎలిజిబిలిటీ & స్కీమ్ ప్రాసెస్:")
    
    if current_age > 70:
        st.error("🔴 వయస్సు 70 సంవత్సరాలు దాటింది. ఏ ఇన్సూరెన్స్ పథకానికీ అర్హత లేదు.")
        member['PMJJBY_Status'] = "N/A"
        member['PMSBY_Status'] = "N/A"
    else:
        if current_age <= 50:
            available_schemes = ["PMJJBY", "PMSBY"]
        else:
            available_schemes = ["PMSBY"]

        chosen_scheme = st.selectbox("పని చేయవలసిన స్కీమ్‌ను ఎంచుకోండి:", available_schemes)
        
        status_key = f"{chosen_scheme}_Status"
        app_date_key = f"{chosen_scheme}_AppDate"
        enrol_date_key = f"{chosen_scheme}_EnrolDate"

        st.markdown(f"### 🏦 {chosen_scheme} వివరాలు & తేదీల ఎంట్రీ")
        
        # బ్యాంక్ వివరాలు
        up_bank = st.text_input("బ్యాంక్ పేరు (Bank Name)", member['BankName'])
        up_branch = st.text_input("బ్రాంచ్ (Branch)", member['Branch'])
        up_acc = st.text_input("అకౌంట్ నంబర్ (Account Number)", member['AccNo'])

        st.write("---")
        st.markdown("#### 📅 తేదీల నమోదు (Dates Entry):")

        # 1. అప్లికేషన్ బ్యాంక్ కి సబ్మిట్ చేసిన తేదీ
        default_app_date = date.today() if member[app_date_key] == "-" else date.fromisoformat(member[app_date_key])
        app_date_input = st.date_input("1. అప్లికేషన్ బ్యాంక్ కి సబ్మిట్ చేసిన తేదీ (Application Submitted Date):", value=default_app_date)

        # 2. బ్యాంక్ వారు ఎన్‌రోల్ చేసిన తేదీ (ఆప్షనల్ / చెక్‌బాక్స్ ద్వారా)
        has_bank_enrolled = st.checkbox("బ్యాంక్ వారు ఎన్‌రోల్ చేసారా? (Bank Enrolled)", value=(member[enrol_date_key] != "-"))
        
        enrol_date_input = "-"
        if has_bank_enrolled:
            default_enrol_date = date.today() if member[enrol_date_key] == "-" else date.fromisoformat(member[enrol_date_key])
            enrol_date_input = st.date_input("2. బ్యాంక్ వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrollment Date):", value=default_enrol_date)

        st.write("")
        if st.button("💾 వివరాలు మరియు తేదీలు సేవ్ చేయి"):
            member['BankName'] = up_bank
            member['Branch'] = up_branch
            member['AccNo'] = up_acc
            member[app_date_key] = str(app_date_input)

            # లాజిక్ అప్డేట్: బ్యాంక్ ఎన్‌రోల్మెంట్ తేదీ ఇస్తే 'Done', లేకపోతే 'Pending at Bank'
            if has_bank_enrolled and enrol_date_input != "-":
                member[status_key] = "Done"
                member[enrol_date_key] = str(enrol_date_input)
                st.success(f"✅ Application enrolled successfully saved! ({member['Name']} - {chosen_scheme})")
            else:
                member[status_key] = "Pending at Bank"
                member[enrol_date_key] = "-"
                st.warning(f"⏳ Application submitted to bank. Status: Pending at Bank ({member['Name']} - {chosen_scheme})")
            
            st.rerun()