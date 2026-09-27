from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Google Sheet link
sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data
def load_data():
  try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    return df
  except Exception as e:
    st.error(f'Data load avvadamlo lopam jarigindi: {e}')
    return None


df = load_data()

if df is not None:
  st.sidebar.header('📁 నావిగేషన్')

  # 1. Mandalam
  mandals = sorted(df['MANDAL'].dropna().unique())
  mandal = st.sidebar.selectbox('మండలం ఎంచుకోండి', mandals)

  if mandal:
    # 2. VO
    filtered_vos = sorted(df[df['MANDAL'] == mandal]['VO'].dropna().unique())
    vo = st.sidebar.selectbox('VO (Village Organization) peru', filtered_vos)

    if vo:
      # 3. SHG
      filtered_shgs = sorted(
          df[(df['MANDAL'] == mandal) & (df['VO'] == vo)]['SHG']
          .dropna()
          .unique()
      )
      shg = st.sidebar.selectbox('SHG group ఎంచుకోండి', filtered_shgs)

      if shg:
        members_df = df[
            (df['MANDAL'] == mandal) & (df['VO'] == vo) & (df['SHG'] == shg)
        ]

        # Sidebar location box
        st.sidebar.markdown('---')
        st.sidebar.info(
            f'📍 **Enchukunna Location:**\n{mandal} ➜ {vo} ➜ {shg}'
        )

        # Header Title
        st.markdown(
            '<div style="text-align: center; color: #1f77b4; font-weight: bold;'
            ' font-size: 20px;">🔑 VOA & SHG Insurance Enrollment Portal</div>',
            unsafe_allow_html=True,
        )
        st.write('---')

        # Pending Summary Report
        st.markdown(
            '### 📊 పెండింగ్ సమ్మరీ రిపోర్ట్ (VOA & Bank Summary)'
        )

        col_p1, col_p2 = st.columns(2)
        with col_p1:
          st.markdown(
              '<div style="padding: 15px; background-color: #eef6fc; border-radius:'
              ' 5px; border-left: 5px solid #1f77b4;">'
              '<b>📌 VOA daggara pending unnavi:</b> 5 applications</div>',
              unsafe_allow_html=True,
          )
        with col_p2:
          st.markdown(
              '<div style="padding: 15px; background-color: #fcf8e3; border-radius:'
              ' 5px; border-left: 5px solid #f0ad4e;">'
              '<b>🏦 Bank nandu pending unnavi:</b> Andhra Bank: 1 | SBI:'
              ' 2</div>',
              unsafe_allow_html=True,
          )

        st.write('')
        st.markdown(f'### 👥 SHG Sabhyula Jabhita (Dashboard & Update)')

        # Prati member ki card tho patu update chese form option
        for idx, row in members_df.reset_index().iterrows():
          m_name = row.get('MEMBER NAME', 'Unknown')
          m_age = row.get('AGE', 30)

          # Status examples
          pmjjby_status = 'Done' if idx % 2 == 0 else 'Pending at VOA'
          pmsby_status = 'Done' if idx % 3 == 0 else 'N/A'

          # Member Card display
          st.markdown(
              f"""
                    <div style="padding: 10px 15px; margin-bottom: 5px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 6px;">
                        🆔 <b>ID: {idx+1}</b> &nbsp;|&nbsp; 
                        👤 <b>{m_name}</b> (Vayassu: {m_age})<br>
                        <span style="font-size: 13px; color: #555;">
                            PMJJBY: <b style="color: #2e7d32;">{pmjjby_status}</b> &nbsp;|&nbsp; 
                            PMSBY: <b style="color: #c62828;">{pmsby_status}</b>
                        </span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )

          # Prati member ki kindha edit/update chesukune option (Expander)
          with st.expander(f'✏️ {m_name} (ID: {idx+1}) vivaramulu update cheyyi'):
            col1, col2 = st.columns(2)
            with col1:
              new_age = st.number_input(
                  'వయస్సు (Age)',
                  value=int(m_age) if pd.notna(m_age) else 30,
                  key=f'age_{idx}',
              )
              scheme_choice = st.selectbox(
                  'స్కీమ్ ఎంచుకోండి', ['PMJJBY', 'PMSBY'], key=f'scheme_{idx}'
              )
            with col2:
              bank_name = st.text_input(
                  'బ్యాంక్ పేరు (Bank Name)',
                  value='Indian Overseas Bank',
                  key=f'bank_{idx}',
              )
              acc_no = st.text_input(
                  'అకౌంట్ నంబర్ (Account Number)',
                  value='10734050040106411',
                  key=f'acc_{idx}',
              )

            if st.button('💾 వివరాలు సేవ్ చేయండి', key=f'save_{idx}'):
              st.success(
                  f'✅ {m_name} యొక్క వివరాలు విజయవంతంగా సేవ్ చేయబడ్డాయి!'
              )
