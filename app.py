from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# గూగుల్ షీట్ లింక్
sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data
def load_data():
  try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    return df
  except Exception as e:
    st.error(f'డేటా లోడ్ అవ్వడంలో లోపం ఏర్పడింది: {e}')
    return None


df = load_data()

if df is not None:
  st.sidebar.header('📁 నావిగేషన్')

  # 1. మండలం
  mandals = sorted(df['MANDAL'].dropna().unique())
  mandal = st.sidebar.selectbox('మండలం ఎంచుకోండి', mandals)

  if mandal:
    # 2. VO
    filtered_vos = sorted(df[df['MANDAL'] == mandal]['VO'].dropna().unique())
    vo = st.sidebar.selectbox('VO (Village Organization) పేరు', filtered_vos)

    if vo:
      # 3. SHG
      filtered_shgs = sorted(
          df[(df['MANDAL'] == mandal) & (df['VO'] == vo)]['SHG']
          .dropna()
          .unique()
      )
      shg = st.sidebar.selectbox('SHG గ్రూప్ ఎంచుకోండి', filtered_shgs)

      if shg:
        members_df = df[
            (df['MANDAL'] == mandal) & (df['VO'] == vo) & (df['SHG'] == shg)
        ]

        # సైడ్‌బార్‌లో ప్రస్తుత లొకేషన్ బాక్స్
        st.sidebar.markdown('---')
        st.sidebar.info(
            f'📍 **ఎంచుకున్న లొకేషన్:**\n{mandal} ➜ {vo} ➜ {shg}'
        )

        # హెడర్ టైటిల్
        st.markdown(
            '<div style="text-align: center; color: #1f77b4; font-weight: bold;'
            ' font-size: 20px;">🔑 VOA & SHG Insurance Enrollment Portal</div>',
            unsafe_allow_html=True,
        )
        st.write('---')

        # పెండింగ్ సమ్మరీ రిపోర్ట్ హెడర్
        st.markdown(
            '### 📊 పెండింగ్ సమ్మరీ రిపోర్ట్ (VOA & Bank Summary)'
        )

        col_p1, col_p2 = st.columns(2)
        with col_p1:
          st.markdown(
              '<div style="padding: 15px; background-color: #eef6fc; border-radius:'
              ' 5px; border-left: 5px solid #1f77b4;">'
              '<b>📌 VOA దగ్గర పెండింగ్ ఉన్నవి:</b> 5 అప్లికేషన్లు</div>',
              unsafe_allow_html=True,
          )
        with col_p2:
          st.markdown(
              '<div style="padding: 15px; background-color: #fcf8e3; border-radius:'
              ' 5px; border-left: 5px solid #f0ad4e;">'
              '<b>🏦 బ్యాంక్ నందు పెండింగ్ ఉన్నవి:</b> ఆంధ్ర బ్యాంక్: 1 | SBI:'
              ' 2</div>',
              unsafe_allow_html=True,
          )

        st.write('')
        st.markdown(f'### 👥 SHG సభ్యుల జాబితా (Dashboard)')

        # సభ్యుల వివరాలను కార్డ్స్ లాగా చూపించడం
        for idx, row in members_df.reset_index().iterrows():
          m_name = row.get('MEMBER NAME', 'Unknown')
          m_age = row.get('AGE', 'N/A')

          # ఉదాహరణ స్టేటస్‌లు
          pmjjby_status = 'Done' if idx % 2 == 0 else 'Pending at VOA'
          pmsby_status = 'Done' if idx % 3 == 0 else 'N/A'

          st.markdown(
              f"""
                    <div style="padding: 10px 15px; margin-bottom: 8px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 6px;">
                        🆔 <b>ID: {idx+1}</b> &nbsp;|&nbsp; 
                        👤 <b>{m_name}</b> (వయస్సు: {m_age})<br>
                        <span style="font-size: 13px; color: #555;">
                            PMJJBY: <b style="color: #2e7d32;">{pmjjby_status}</b> &nbsp;|&nbsp; 
                            PMSBY: <b style="color: #c62828;">{pmsby_status}</b>
                        </span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )
