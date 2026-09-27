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
    # Normalize MANDAL column to handle case sensitivity and extra spaces
    if 'MANDAL' in df.columns:
      df['MANDAL'] = df['MANDAL'].astype(str).str.strip().str.title()
    return df
  except Exception as e:
    st.error(f'Data load avvadamlo lopam jarigindi: {e}')
    return None


df = load_data()

if df is not None:
  st.sidebar.header('📁 నావిగేషన్')
  app_mode = st.sidebar.radio(
      'పేజీ ఎంచుకోండి:',
      ['🏠 ఎన్‌రోల్మెంట్ డాష్‌బోర్డ్ (Portal)', '📊 జిల్లా అబ్‌స్ట్రాక్ట్ & రిపోర్ట్'],
  )

  if app_mode == '🏠 ఎన్‌రోల్మెంట్ డాష్‌బోర్డ్ (Portal)':
    mandals = sorted(df['MANDAL'].dropna().unique())
    mandal = st.sidebar.selectbox('మండలం ఎంచుకోండి', mandals)

    if mandal:
      filtered_vos = sorted(
          df[df['MANDAL'] == mandal]['VO'].dropna().unique()
      )
      vo = st.sidebar.selectbox('VO (Village Organization) peru', filtered_vos)

      if vo:
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

          st.sidebar.markdown('---')
          st.sidebar.info(
              f'📍 **Enchukunna Location:**\n{mandal} ➜ {vo} ➜ {shg}'
          )

          st.markdown(
              '<div style="text-align: center; color: #1f77b4; font-weight:'
              ' bold; font-size: 20px;">🔑 VOA & SHG Insurance Enrollment'
              ' Portal</div>',
              unsafe_allow_html=True,
          )
          st.write('---')

          st.markdown(f'### 👥 SHG Sabhyula Jabhita (Dashboard)')

          for idx, row in members_df.reset_index().iterrows():
            m_name = str(row.get('MEMBER NAME', 'Unknown'))
            m_id = str(row.get('MEMBER ID', f'ID-{idx+1}'))
            m_age = row.get('AGE', 35)
            if pd.isna(m_age):
              m_age = 35
            else:
              m_age = int(m_age)

            if m_age > 70:
              pmjjby_elig = 'Not Applicable'
              pmsby_elig = 'Not Applicable'
            elif 50 <= m_age <= 70:
              pmjjby_elig = 'Not Applicable'
              pmsby_elig = 'Eligible (Not Enrolled)'
            else:
              pmjjby_elig = 'Eligible (Not Enrolled)'
              pmsby_elig = 'Eligible (Not Enrolled)'

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

            # Member Update Form
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
                # PMJJBY
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
                          ' Optional) - PMJJBY',
                          value=None,
                          key=f'pmjjby_b_date_opt_{idx}',
                      )

                st.markdown('---')

                # PMSBY
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
                        ' Optional) - PMSBY',
                        value=None,
                        key=f'pmsby_b_date_opt_{idx}',
                    )

              if st.button(
                  f'💾 {m_name} వివరాలు సేవ్ చేయండి', key=f'save_btn_{idx}'
              ):
                st.success(
                    f'✅ {m_name} యొక్క వివరాలు విజయవంతంగా అప్‌డేట్ చేయబడ్డాయి!'
                )

  elif app_mode == '📊 జిల్లా అబ్‌స్ట్రాక్ట్ & రిపోర్ట్':
    st.markdown('## 📊 మండలాల వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్ (Abstract Summary)')
    st.write(
        'ఇక్కడ జిల్లాలోని అన్ని మండలాల వారీగా PMJJBY (18-50) మరియు PMSBY (18-70)'
        ' ఎలిజిబిలిటీ టార్గెట్, బ్యాంక్ సబ్మిటెడ్, బ్యాంక్ ఎన్‌రోల్డ్ మరియు'
        ' బ్యాలెన్స్ వివరాల అబ్‌స్ట్రాక్ట్ టేబుల్ కింద గ్రాండ్ టోటల్‌తో సహా'
        ' కనిపిస్తుంది.'
    )
    st.write('---')

    temp_df = df.copy()
    temp_df['AGE'] = pd.to_numeric(temp_df['AGE'], errors='coerce').fillna(35)

    col_pmjjby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at'
        ' Bank) - PMJJBY'
    )
    col_pmjjby_bank = (
        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date - Optional) -'
        ' PMJJBY'
    )
    col_pmsby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at'
        ' Bank) - PMSBY'
    )
    col_pmsby_bank = (
        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date - Optional) -'
        ' PMSBY'
    )

    temp_df['PMJJBY_Eligible'] = temp_df['AGE'].apply(
        lambda x: 1 if 18 <= x < 50 else 0
    )
    temp_df['PMSBY_Eligible'] = temp_df['AGE'].apply(
        lambda x: 1 if 18 <= x <= 70 else 0
    )

    for c in [
        col_pmjjby_sub,
        col_pmjjby_bank,
        col_pmsby_sub,
        col_pmsby_bank,
    ]:
      if c not in temp_df.columns:
        temp_df[c] = None

    temp_df['PMJJBY_Submitted_Count'] = (
        temp_df[col_pmjjby_sub].notna().astype(int)
    )
    temp_df['PMJJBY_Bank_Count'] = temp_df[col_pmjjby_bank].notna().astype(int)
    temp_df['PMJJBY_Already_Count'] = 0

    temp_df['PMSBY_Submitted_Count'] = (
        temp_df[col_pmsby_sub].notna().astype(int)
    )
    temp_df['PMSBY_Bank_Count'] = temp_df[col_pmsby_bank].notna().astype(int)
    temp_df['PMSBY_Already_Count'] = 0

    all_mandals = sorted(temp_df['MANDAL'].dropna().unique())

    abstract_df = (
        temp_df.groupby('MANDAL')
        .agg(
            PMJJBY_Eligible=('PMJJBY_Eligible', 'sum'),
            PMJJBY_Already_Enrolled=('PMJJBY_Already_Count', 'sum'),
            PMJJBY_Submitted_Bank=('PMJJBY_Submitted_Count', 'sum'),
            PMJJBY_Bank_Enrolled=('PMJJBY_Bank_Count', 'sum'),
            PMSBY_Eligible=('PMSBY_Eligible', 'sum'),
            PMSBY_Already_Enrolled=('PMSBY_Already_Count', 'sum'),
            PMSBY_Submitted_Bank=('PMSBY_Submitted_Count', 'sum'),
            PMSBY_Bank_Enrolled=('PMSBY_Bank_Count', 'sum'),
        )
        .reindex(all_mandals)
        .fillna(0)
        .reset_index()
    )

    abstract_df['PMJJBY_Balance'] = (
        abstract_df['PMJJBY_Eligible']
        - abstract_df['PMJJBY_Already_Enrolled']
        - abstract_df['PMJJBY_Bank_Enrolled']
    )
    abstract_df['PMSBY_Balance'] = (
        abstract_df['PMSBY_Eligible']
        - abstract_df['PMSBY_Already_Enrolled']
        - abstract_df['PMSBY_Bank_Enrolled']
    )

    tot_row = {
        'MANDAL': 'GRAND TOTAL',
        'PMJJBY_Eligible': abstract_df['PMJJBY_Eligible'].sum(),
        'PMJJBY_Already_Enrolled': abstract_df['PMJJBY_Already_Enrolled'].sum(),
        'PMJJBY_Submitted_Bank': abstract_df['PMJJBY_Submitted_Bank'].sum(),
        'PMJJBY_Bank_Enrolled': abstract_df['PMJJBY_Bank_Enrolled'].sum(),
        'PMJJBY_Balance': abstract_df['PMJJBY_Balance'].sum(),
        'PMSBY_Eligible': abstract_df['PMSBY_Eligible'].sum(),
        'PMSBY_Already_Enrolled': abstract_df['PMSBY_Already_Enrolled'].sum(),
        'PMSBY_Submitted_Bank': abstract_df['PMSBY_Submitted_Bank'].sum(),
        'PMSBY_Bank_Enrolled': abstract_df['PMSBY_Bank_Enrolled'].sum(),
        'PMSBY_Balance': abstract_df['PMSBY_Balance'].sum(),
    }

    abstract_df.loc[len(abstract_df)] = tot_row
    abstract_df.insert(0, 'S.NO', list(range(1, len(abstract_df))) + ['-'])

    abstract_df.columns = [
        'S.NO',
        'MANDAL NAME',
        'NO OF MEMBERS ELEGIBLE FOR PMJJBY(18-50)',
        'Already Enrolled (PMJJBY)',
        'Not Enrolled-అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసినవి - PMJJBY',
        'బ్యాంకు వారు ఎన్‌రోల్ చేసినవి - PMJJBY',
        'BALANCE (PMJJBY)',
        'NO OF MEMBERS ELEGIBLE FOR PMSBY(18-70)',
        'Already Enrolled (PMSBY)',
        'Not Enrolled-అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసినవి - PMSBY',
        'బ్యాంకు వారు ఎన్‌రోల్ చేసినవి - PMSBY',
        'BALANCE (PMSBY)',
    ]

    st.subheader(
        f'📋 Mandal-wise Abstract Summary with Grand Total (Total Mandals:'
        f' {len(abstract_df)-1})'
    )
    st.dataframe(abstract_df, use_container_width=True)

    csv_data = abstract_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=(
            '📥 అబ్‌స్ట్రాక్ట్ గ్రాండ్ టోటల్ రిపోర్ట్‌ని CSV రూపంలో డౌన్‌లోడ్'
            ' చేసుకోండి'
        ),
        data=csv_data,
        file_name='District_Insurance_Abstract_With_Total.csv',
        mime='text/csv',
    )
