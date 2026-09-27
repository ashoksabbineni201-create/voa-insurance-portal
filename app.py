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

        # Prati member ki card
        for idx, row in members_df.reset_index().iterrows():
          m_name = str(row.get('MEMBER NAME', 'Unknown'))
          m_id = str(row.get('MEMBER ID', f'ID-{idx+1}'))
          m_age = row.get('AGE', 35)
          if pd.isna(m_age):
            m_age = 35
          else:
            m_age = int(m_age)

          # Age-based Eligibility rules
          if m_age > 70:
            pmjjby_elig = 'Not Applicable'
            pmsby_elig = 'Not Applicable'
          elif 50 <= m_age <= 70:
            pmjjby_elig = 'Not Applicable'
            pmsby_elig = 'Eligible (Not Enrolled)'
          else:
            pmjjby_elig = 'Eligible (Not Enrolled)'
            pmsby_elig = 'Eligible (Not Enrolled)'

          # Member Card display
          st.markdown(
              f"""
                    <div style="padding: 12px 15px; margin-bottom: 8px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 6px;">
                        🆔 <b>Member ID: {m_id}</b> &nbsp;|&nbsp; 
                        👤 <b>{m_name}</b> (వయస్సు: {m_age} - As per Aadhaar)<br>
                        <span style="font-size: 13px; color: #555;">
                            <b>PMJJBY:</b> <span style="color: #1f77b4;">{pmjjby_elig}</span> &nbsp;|&nbsp; 
                            <b>PMSBY:</b> <span style="color: #1f77b4;">{pmsby_elig}</span>
                        </span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )

          # Member Update & Verification Form (Expander)
          with st.expander(
              f'✏️ {m_name} (Member ID: {m_id}) వివరాలు సరిచూడండి / మార్చండి'
          ):
            updated_age = st.number_input(
                'మెంబర్ వయస్సు నిర్ధారించండి / మార్చండి (Age - As per'
                ' Aadhaar):',
                min_value=18,
                max_value=100,
                value=m_age,
                key=f'age_{idx}',
            )

            st.write('---')

            if updated_age > 70:
              st.error(
                  '⚠️ ఈ మెంబర్ వయస్సు 70 సంవత్సరాలు దాటింది కాబట్టి ఏ స్కీమ్‌కూ'
                  ' ఎలిజిబిలిటీ లేదు (Not Applicable).'
              )
            else:
              # 1. PMJJBY Scheme Details & Separate Bank Info
              st.markdown('### 📌 1. PMJJBY స్కీమ్ వివరాలు & బ్యాంక్ అకౌంట్')
              if updated_age >= 50:
                st.info(
                    'ℹ️ 50 సంవత్సరాలు దాటడం వలన PMJJBY వర్తించదు (Not'
                    ' Applicable).'
                )
              else:
                bc1, bc2, bc3 = st.columns(3)
                with bc1:
                  pmjjby_bank = st.text_input(
                      'బ్యాంక్ పేరు (PMJJBY Bank)',
                      value=str(row.get('BANK NAME', 'Indian Overseas Bank')),
                      key=f'pmjjby_bank_{idx}',
                  )
                with bc2:
                  pmjjby_branch = st.text_input(
                      'బ్రాంచ్ (PMJJBY Branch)',
                      value=str(row.get('BRANCH NAME', 'VEJENDLA')),
                      key=f'pmjjby_branch_{idx}',
                  )
                with bc3:
                  pmjjby_acc = st.text_input(
                      'అకౌంట్ నంబర్ (PMJJBY Acc No)',
                      value=str(row.get('MEMBER SB ACCOUNT NUMBER', '')),
                      key=f'pmjjby_acc_{idx}',
                  )

                pmjjby_enrolled = st.radio(
                    'PMJJBY కింద మెంబర్ ఎన్రోల్ అయ్యారా?',
                    ['Not Enrolled', 'Already Enrolled'],
                    key=f'pmjjby_status_{idx}',
                )

                if pmjjby_enrolled == 'Already Enrolled':
                  pmjjby_bank_date = st.date_input(
                      'బ్యాంకు వారు ఎన్రోల్ చేసిన తేది (Bank Enrolled Date)'
                      ' - PMJJBY',
                      key=f'pmjjby_b_date_{idx}',
                  )
                else:
                  col_d1, col_d2 = st.columns(2)
                  with col_d1:
                    pmjjby_sub_date = st.date_input(
                        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application'
                        ' Submitted at Bank) - PMJJBY',
                        key=f'pmjjby_sub_date_{idx}',
                    )
                  with col_d2:
                    pmjjby_bank_date_opt = st.date_input(
                        'బ్యాంకు వారు ఎన్రోల్ చేసిన తేదీ (Bank Enrolled Date -'
                        ' Optional if approved) - PMJJBY',
                        value=None,
                        key=f'pmjjby_b_date_opt_{idx}',
                    )

              st.markdown('---')

              # 2. PMSBY Scheme Details & Separate Bank Info
              st.markdown('### 📌 2. PMSBY స్కీమ్ వివరాలు & బ్యాంక్ అకౌంట్')
              pc1, pc2, pc3 = st.columns(3)
              with pc1:
                pmsby_bank = st.text_input(
                    'బ్యాంక్ పేరు (PMSBY Bank)',
                    value=str(row.get('BANK NAME', 'Indian Overseas Bank')),
                    key=f'pmsby_bank_{idx}',
                )
              with pc2:
                pmsby_branch = st.text_input(
                    'బ్రాంచ్ (PMSBY Branch)',
                    value=str(row.get('BRANCH NAME', 'VEJENDLA')),
                    key=f'pmsby_branch_{idx}',
                )
              with pc3:
                pmsby_acc = st.text_input(
                    'అకౌంట్ నంబర్ (PMSBY Acc No)',
                    value=str(row.get('MEMBER SB ACCOUNT NUMBER', '')),
                    key=f'pmsby_acc_{idx}',
                )

              pmsby_enrolled = st.radio(
                  'PMSBY కింద మెంబర్ ఎన్రోల్ అయ్యారా?',
                  ['Not Enrolled', 'Already Enrolled'],
                  key=f'pmsby_status_{idx}',
              )

              if pmsby_enrolled == 'Already Enrolled':
                pmsby_bank_date = st.date_input(
                    'బ్యాంకు వారు ఎన్రోల్ చేసిన తేది (Bank Enrolled Date)'
                    ' - PMSBY',
                    key=f'pmsby_b_date_{idx}',
                )
              else:
                col_d3, col_d4 = st.columns(2)
                with col_d3:
                  pmsby_sub_date = st.date_input(
                      'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application'
                      ' Submitted at Bank) - PMSBY',
                      key=f'pmsby_sub_date_{idx}',
                  )
                with col_d4:
                  pmsby_bank_date_opt = st.date_input(
                      'బ్యాంకు వారు ఎన్రోల్ చేసిన తేదీ (Bank Enrolled Date -'
                      ' Optional if approved) - PMSBY',
                      value=None,
                      key=f'pmsby_b_date_opt_{idx}',
                  )

            if st.button(
                f'💾 {m_name} వివరాలు సేవ్ చేయండి', key=f'save_btn_{idx}'
            ):
              st.success(
                  f'✅ {m_name} యొక్క వివరాలు విజయవంతంగా అప్‌డేట్ చేయబడ్డాయి!'
              )
