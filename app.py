from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

st.markdown(
    """
    <style>
    .main-title { font-size: 24px; font-weight: bold; color: #1f77b4; text-align: center; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="main-title">🏛️ VOA & SHG Insurance Enrollment Portal</p>',
    unsafe_allow_html=True,
)
st.write('---')

# Google Sheet నుండి డేటాను లోడ్ చేయడం
sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data
def load_data():
  try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()  # అదనపు స్పేస్‌లను తొలగించడం
    return df
  except Exception as e:
    st.error(f'డేటా లోడ్ అవ్వడంలో లోపం ఏర్పడింది: {e}')
    return None


df = load_data()

if df is not None:
  st.sidebar.header('📁 నావిగేషన్')

  # మండలం సెలెక్ట్ చేసుకోవడం
  mandals = sorted(df['MANDAL'].dropna().unique())
  mandal = st.sidebar.selectbox('మండలం ఎంచుకోండి', mandals)

  if mandal:
    filtered_vos = sorted(df[df['MANDAL'] == mandal]['VO'].dropna().unique())
    vo = st.sidebar.selectbox('VO ఎంచుకోండి', filtered_vos)

    if vo:
      filtered_shgs = sorted(
          df[(df['MANDAL'] == mandal) & (df['VO'] == vo)]['SHG']
          .dropna()
          .unique()
      )
      shg = st.sidebar.selectbox('SHG ఎంచుకోండి', filtered_shgs)

      if shg:
        members_df = df[
            (df['MANDAL'] == mandal)
            & (df['VO'] == vo)
            & (df['SHG'] == shg)
        ]

        st.success(
            f'ఎంచుకున్న గ్రూప్: **{shg}** (మొత్తం సభ్యులు: {len(members_df)})'
        )
        st.subheader('📋 సభ్యుల జాబితా & వివరాలు')

        # ఎర్రర్ రాకుండా నేరుగా డేటాను ప్రదర్శించడం
        st.dataframe(members_df)
