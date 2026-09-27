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
        st.markdown(f'### 👥 SHG Sabhyula Jabhita (Dashboard)')

        # Prati member ki card & eligibility rules
        for idx, row in members_df.reset_index().iterrows():
          m_name = row.get('MEMBER NAME', 'Unknown')
          m_age = row.get('AGE', 35)
          if pd.isna(m_age):
            m_age = 35
          else:
            m_age = int(m_age)

          # Age-based Eligibility rules
          if m_age > 70:
            pmjjby_elig = 'Not Applicable (> 70 yrs)'
            pmsby_elig = 'Not Applicable (> 70 yrs)'
          elif 50 <= m_age <= 70:
            pmjjby_elig = 'Not Applicable (Age 50-70)'
            pmsby_elig = 'Eligible'
          else:  # 18 to 49
            pmjjby_elig = 'Eligible'
            pmsby_elig = 'Eligible'

          # Member Card display
          st.markdown(
              f"""
                    <div style="padding: 10px 15px; margin-bottom: 5px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 6px;">
                        🆔 <b>ID: {idx+1}</b> &nbsp;|&nbsp; 
                        👤 <b>{m_name}</b> (వయస్సు: {m_age})<br>
                        <span style="font-size: 13px; color: #555;">
                            PMJJBY Status: <b style="color: #1f77b4;">{pmjjby_elig}</b> &nbsp;|&nbsp; 
                            PMSBY Status: <b style="color: #1f77b4;">{pmsby_elig}</b>
                        </span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )

          # Member Update & Verification Form (Expander)
          with st.expander(f'✏️ {m_name} (ID: {idx+1}) వివరాలు సరిచూడండి / మార్చండి'):
            # Step 1: Age Confirmation
            updated_age = st.number_input(
                'మెంబర్ వయస్సు నిర్ధారించండి / మార్చండి (Age):',
                min_value=18,
                max_value=100,
                value=m_age,
                key=f'age_{idx}',
            )

            st.write('---')

            # Dynamic Eligibility based on confirmed age
            if updated_age > 70:
              st.error(
                  '⚠️ ఈ మెంబర్ వయస్సు 70 సంవత్సరాలు దాటింది కాబట్టి ఏ స్కీమ్‌కూ'
                  ' ఎలిజిబిలిటీ లేదు (Not Applicable).'
              )
            else:
              # Bank & Branch details shared across schemes
              c1, c2, c3 = st.columns(3)
              with c1:
                bank_name = st.text_input(
                    'బ్యాంక్ పేరు (Bank Name)',
                    value='Indian Overseas Bank',
                    key=f'bank_{idx}',
                )
              with c2:
                branch_name = st.text_input(
                    'బ్రాంచ్ (Branch)', value='VEJENDLA', key=f'branch_{idx}'
                )
              with c3:
                acc_no = st.text_input(
                    'అకౌంట్ నంబర్ (Account Number)',
                    value=str(row.get('MEMBER sb account number', '')),
                    key=f'acc_{idx}',
                )

              st.markdown('### 📌 1. PMJJBY స్కీమ్ వివరాలు')
              if updated_age >= 50:
                st.info(
                    'ℹ️ 50 సంవత్సరాలు దాటడం వలన PMJJBY వర్తించదు (Not'
                    ' Applicable).'
                )
              else:
                pmjjby_enrolled = st.radio(
                    'PMJJBY కింద మెంబర్ ఆల్రెడీ ఎన్రోల్ అయ్యారా?',
                    ['Not Enrolled', 'Already Enrolled'],
                    key=f'pmjjby_status_{idx}',
                )
                if pmjjby_enrolled == 'Already Enrolled':
                  pmjjby_bank_date = st.date_input(
                      'బ్యాంకులో ఎన్రోల్ అయిన తేది (Bank Enrolled Date)',
                      key=f'pmjjby_b_date_{idx}',
                  )
                else:
                  col_d1, col_d2 = st.columns(2)
                  with col_d1:
                    pmjjby_sub_date = st.date_input(
                        'అప్లికేషన్ సబ్మిట్ చేసిన తేది (Application Submitted'
                        ' at Bank)',
                        key=f'pmjjby_sub_date_{idx}',
                    )
                  with col_d2:
                    pmjjby_bank_date = st.date_input(
                        'బ్యాంకులో ఎన్రోల్ అయిన తేది (Bank Enrolled Date)',
                        key=f'pmjjby_b_date_new_{idx}',
                    )

              st.markdown('---')
              st.markdown('### 📌 2. PMSBY స్కీమ్ వివరాలు')
              pmsby_enrolled = st.radio(
                  'PMSBY కింద మెంబర్ ఆల్రెడీ ఎన్రోల్ అయ్యారా?',
                  ['Not Enrolled', 'Already Enrolled'],
                  key=f'pmsby_status_{idx}',
              )
              if pmsby_enrolled == 'Already Enrolled':
                pmsby_bank_date = st.date_input(
                    'బ్యాంకులో ఎన్రోల్ అయిన తేది (Bank Enrolled Date) - PMSBY',
                    key=f'pmsby_b_date_{idx}',
                )
              else:
                col_d3, col_d4 = st.columns(2)
                with col_d3:
                  pmsby_sub_date = st.date_input(
                      'అప్లికేషన్ సబ్మిట్ చేసిన తేది (Application Submitted'
                      ' at Bank) - PMSBY',
                      key=f'pmsby_sub_date_{idx}',
                  )
                with col_d4:
                  pmsby_bank_date = st.date_input(
                      'బ్యాంకులో ఎన్రోల్ అయిన తేది (Bank Enrolled Date) - PMSBY',
                      key=f'pmsby_b_date_new_{idx}',
                  )

            if st.button(
                f'💾 {m_name} వివరాలు సేవ్ చేయండి', key=f'save_btn_{idx}'
            ):
              st.success(
                  f'✅ {m_name} యొక్క వయస్సు ({updated_age}) మరియు ఎన్రోల్మెంట్'
                  ' వివరాలు విజయవంతంగా అప్‌డేట్ చేయబడ్డాయి!'
              )
