from datetime import date
import io
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title='Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .portal-header {
        background: linear-gradient(135deg, #fff176 0%, #ffee58 100%);
        padding: 25px;
        border-radius: 20px;
        color: #d32f2f !important;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border: 2px solid #fbc02d;
    }
    .portal-header h1 { 
        color: #c62828 !important; 
        font-size: 26px !important; 
        font-weight: 800; 
    }
    .portal-header p { 
        color: #b71c1c !important; 
        font-size: 15px !important; 
        margin-top: 5px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
        }
        response = requests.get(sheet_url, headers=headers, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text), dtype=str)
            df.columns = df.columns.str.strip()
            for col in ['MANDAL', 'VO', 'SHG', 'BANK NAME', 'BRANCH NAME']:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip().str.upper()
            return df
        return None
    except Exception:
        return None


with st.spinner('డేటా లోడ్ చేయబడుతోంది...'):
    df = load_data()

if df is None:
    st.error(
        '❌ డేటా లోడ్ అవ్వడంలో సమస్య ఏర్పడింది. దయచేసి పేజీని రిఫ్రెష్ (Refresh)'
        ' చేయండి.'
    )
else:
    # Header Title
    st.markdown(
        '<div class="portal-header"><h1>గుంటూరు జిల్లా - SHG సభ్యుల బీమా (PMJJBY & PMSBY) ఎన్‌రోల్‌మెంట్ పోర్టల్</h1><p>సంఘ సభ్యులందరికీ సులభంగా ఇన్సూరెన్స్ నమోదు మరియు ట్రాకింగ్ చేయు విధానం</p></div>',
        unsafe_allow_html=True,
    )

    # Basic Navigation
    app_mode = st.selectbox(
        '📌 సెక్షన్ ఎంచుకోండి:',
        [
            'డాష్‌‌బోర్డ్ (Dashboard)',
            'మండలం వారీగా రిపోర్ట్ (Mandal Wise)',
            'సభ్యుల జాబితా (Member Level)',
        ],
    )

    st.markdown('---')

    if app_mode == 'డాష్‌‌‌‌బోర్డ్ (Dashboard)':
        st.info(
            '👉 దయచేసి క్రింద మీ మండలాన్ని ఎంచుకోండి.'
        )
        mandals = ['-- ఎంచుకోండి --'] + sorted(
            df['MANDAL'].dropna().unique().tolist()
        )
        selected_mandal = st.selectbox('మండలం ఎంచుకోండి:', mandals)

        if selected_mandal != '-- ఎంచుకోండి --':
            mandal_df = df[df['MANDAL'] == selected_mandal]
            st.success(f'మొత్తం రికార్డులు: {len(mandal_df)}')
            st.dataframe(mandal_df, use_container_width=True)

    elif app_mode == 'మండలం వారీగా రిపోర్ట్ (Mandal Wise)':
        st.markdown('## 📍 మండలం వారీగా సారాంశం')
        mandal_summary = df.groupby('MANDAL').size().reset_index(name='Total Members')
        st.dataframe(mandal_summary, use_container_width=True)

    else:
        st.markdown('## 👥 పూర్తి సభ్యుల జాబితా')
        st.dataframe(df, use_container_width=True)
