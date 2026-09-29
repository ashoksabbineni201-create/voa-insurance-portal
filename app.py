from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS for styling categories in sidebar
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .portal-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 12px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
    }
    .portal-header h1 { color: #ffffff !important; font-size: 26px !important; }
    
    .section-title-pmjjby {
        color: #1565C0;
        border-bottom: 2px solid #1565C0;
        padding-bottom: 5px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .section-title-pmsby {
        color: #2E7D32;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 5px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        for col in ['MANDAL', 'VO', 'SHG', 'BANK NAME', 'BRANCH NAME']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
        return df
    except Exception as e:
        st.error(f'డేటా లోడ్ చేయడంలో విఫలమైంది: {e}')
        return None


df = load_data()

if df is not None:
    col_pmjjby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMJJBY'
    )
    col_pmjjby_bank = (
        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY'
    )
    col_pmsby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMSBY'
    )
    col_pmsby_bank = (
        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMSBY'
    )

    for c in [
        col_pmjjby_sub,
        col_pmjjby_bank,
        col_pmsby_sub,
        col_pmsby_bank,
    ]:
        if c not in df.columns:
            df[c] = None

    if 'saved_entries_dict' not in st.session_state:
        st.session_state.saved_entries_dict = {}

    export_df_base = df.copy()
    if len(st.session_state.saved_entries_dict) > 0:
        for m_id, saved_row in st.session_state.saved_entries_dict.items():
            idx_match = export_df_base[
                export_df_base['MEMBER ID'].astype(str) == str(m_id)
            ].index
            if not idx_match.empty:
                for k, v in saved_row.items():
                    if k not in export_df_base.columns:
                        export_df_base[k] = None
                    export_df_base[k] = export_df_base[k].astype(object)
                    export_df_base.loc[idx_match, k] = str(v) if v is not None else None

    export_df_base['NUM_AGE'] = pd.to_numeric(
        export_df_base['AGE'], errors='coerce'
    ).fillna(0)

    # Sidebar Navigation Setup with 3 Categorized Sections
    st.sidebar.markdown('📁 **NAVIGATOR / నావిగేషన్ మెను**')
    st.sidebar.markdown('---')

    # Category 1: Dashboard
    st.sidebar.markdown('**🏠 1. Dashboard**')
    opt_dash = st.sidebar.radio(
        'డ్యాష్‌బోర్డ్ ఎంచుకోండి:',
        ['🏠 Enrollment Dashboard (Portal)'],
        label_visibility='collapsed'
    )

    st.sidebar.markdown('---')

    # Category 2: Master Reports
    st.sidebar.markdown('**📋 2. Master Reports**')
    opt_master = st.sidebar.radio(
        'మాస్టర్ రిపోర్ట్స్ ఎంచుకోండి:',
        [
            '📍 Mandal Wise Abstract Report',
            '📊 Mandal & VO Wise Abstract Report',
            '📥 Detailed Lists & Pending Reports',
            '👥 SHG Member Level Detailed Report'
        ],
        label_visibility='collapsed'
    )

    st.sidebar.markdown('---')

    # Category 3: Bank Reports
    st.sidebar.markdown('**🏛️ 3. Bank Reports**')
    opt_bank = st.sidebar.radio(
        'బ్యాంక్ రిపోర్ట్స్ ఎంచుకోండి:',
        [
            '🏛️ Bank Wise Report',
            '📊 Bank Branch Wise Abstract Report'
        ],
        label_visibility='collapsed'
    )

    st.sidebar.markdown('---')

    # Map the selected option to app_mode
    if opt_dash:
        app_mode = opt_dash
    if 'opt_master' in locals() and st.sidebar.session_state.get('previous_master') != opt_master:
        # Handling multiple radios gracefully by prioritizing the last active section or combining them
        pass

    # Simplified unified routing based on user selection mapping
    all_nav_options = {
        '🏠 Enrollment Dashboard (Portal)': 0,
        '📍 Mandal Wise Abstract Report': 1,
        '📊 Mandal & VO Wise Abstract Report': 2,
        '📥 Detailed Lists & Pending Reports': 3,
        '👥 SHG Member Level Detailed Report': 4,
        '🏛️ Bank Wise Report': 5,
        '📊 Bank Branch Wise Abstract Report': 6
    }

    # Let's use a cleaner selectbox/radio approach per section or unified radio mapping:
    # To keep single active state cleanly, we can use selectbox or a unified radio with section headers using markdown labels:
    
    # Alternative clean implementation using radio with grouped labels:
    st.sidebar.empty() # clear previous if needed
