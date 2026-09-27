from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Google Sheet link
sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data(ttl=60)
def load_data():
  try:
    df = pd.read_csv(sheet_url)
    df.columns = df.columns.str.strip()
    if 'MANDAL' in df.columns:
      df['MANDAL'] = df['MANDAL'].astype(str).str.strip().str.title()
    return df
  except Exception as e:
    st.error(f'Data load avvadamlo lopam jarigindi: {e}')
    return None


df = load_data()

if df is not None:
  # డేటా ఫ్రేమ్‌లో అవసరమైన డేట్ కాలమ్స్ లేకపోతే నల్ (None) తో క్రియేట్ చేయడం
  col_pmjjby_sub = (
      'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at'
      ' Bank) - PMJJBY'
  )
  col_pmjjby_bank = (
      'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY'
  )
  col_pmsby_sub = (
      'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at'
      ' Bank) - PMSBY'
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
      df[c] = pd.NaT

  st.sidebar.header('📁 నావిగేషన్')

  # --- కేవలం ఎంట్రీలు / అప్‌డేట్లు చేసిన డేటా మాత్రమే డౌన్‌లోడ్ అయ్యేలా ఫిల్టర్ ---
  st.sidebar.markdown('---')
  st.sidebar.markdown('### 📥 రిపోర్ట్ డౌన్‌లోడ్')

  entered_df = df[
      df[col_pmjjby_sub].notna()
      | df[col_pmjjby_bank].notna()
      | df[col_pmsby_sub].notna()
      | df[col_pmsby_bank].notna()
  ]

  entered_csv_report = entered_df.to_csv(index=False).encode('utf-8')
  st.sidebar.download_button(
      label='📥 ఎంట్రీ చేసిన వివరాలు మాత్రమే డౌన్‌లోడ్ చేసుకోండి (CSV)',
      data=entered_csv_report,
      file_name='Enrolled_Members_Report.csv',
      mime='text/csv',
  )
  st.sidebar.markdown('---')

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

            raw_age = row.get('AGE', 35)
            if pd.isna(raw_age):
              raw_age = 35
            else:
              raw_age = int(raw_age)

            st.markdown(
                f"""
                        <div style="padding: 12px 15px; margin-bottom: 8px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 6px;">
                            🆔 <b>Member ID: {m_id}</b> &nbsp;|&nbsp; 
                            👤 <b>{m_name}</b> (డేటాబేస్ వయస్సు: {raw_age} సంవత్సరాలు)<br>
                        </div>
                        """,
                unsafe_allow_html=True,
            )

            with st.expander(
                f'✏️ {m_name} (Member ID: {m_id}) వయస్సు నిర్ధారణ & వివరాలు'
            ):
              entered_age = st.number_input(
                  'మెంబర్ వయస్సు నిర్ధారించండి / మార్చండి (Age - As per'
                  ' Aadhaar):',
                  min_value=1,
                  max_value=100,
                  value=raw_age,
                  key=f'age_{idx}',
              )

              age_confirmed = st.button(
                  f'✔️ {m_name} వయస్సును నిర్ధారించండి (Confirm Age)',
                  key=f'confirm_age_btn_{idx}',
              )

              session_key = f'confirmed_age_val_{idx}'
              if age_confirmed:
                st.session_state[session_key] = entered_age

              active_age = st.session_state.get(session_key, raw_age)

              st.write('---')
              st.info(
                  f'📌 ప్రస్తుతం పరిగణించబడిన వయస్సు: **{active_age} సంవత్సరాలు**'
              )

              if active_age < 18:
                st.error(
                    '❌ హెచ్చరిక: మెంబర్ వయస్సు 18 సంవత్సరాల కంటే తక్కువగా ఉంది.'
                    ' కాబట్టి నిబంధనల ప్రకారం ఎటువంటి స్కీమ్ ఎంట్రీకి అవకాశం'
                    ' లేదు.'
                )
              elif active_age > 70:
                st.error(
                    '❌ హెచ్చరిక: మెంబర్ వయస్సు 70 సంవత్సరాలు దాటింది. కాబట్టి'
                    ' PMJJBY మరియు PMSBY ఏ స్కీమ్‌కూ ఎలిజిబిలిటీ లేదు.'
                )
              else:
                st.success(
                    f'✅ వయస్సు నిబంధనలకు అనుగుణంగా ఉంది. వర్తించే స్కీమ్‌ల'
                    ' వివరాలు కింద ఇవ్వబడ్డాయి.'
                )

                # ==================== 1. PMJJBY Section ====================
                if active_age <= 50:
                  st.markdown('### 📌 1. PMJJBY స్కీమ్ వివరాలు (18 నుండి 50 లోపు)')
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

                  pmjjby_sub_date = None
                  pmjjby_b_date = None

                  if pmjjby_enrolled == 'Already Enrolled':
                    pmjjby_b_date = st.date_input(
                        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) -'
                        ' PMJJBY',
                        value=None,
                        key=f'pmjjby_b_date_already_{idx}',
                    )
                  else:
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                      pmjjby_sub_date = st.date_input(
                          'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application'
                          ' Submitted at Bank) - PMJJBY',
                          value=None,
                          key=f'pmjjby_sub_date_{idx}',
                      )
                    with col_d2:
                      pmjjby_b_date = st.date_input(
                          'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) -'
                          ' PMJJBY',
                          value=None,
                          key=f'pmjjby_b_date_opt_{idx}',
                      )

                  if st.button(
                      f'💾 {m_name} - PMJJBY వివరాలు సేవ్ చేయండి',
                      key=f'save_pmjjby_{idx}',
                  ):
                    if pmjjby_enrolled == 'Already Enrolled':
                      if pmjjby_b_date is None:
                        st.error(
                            '⚠️ దయచేసి "బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ" (Bank'
                            ' Enrolled Date) ఎంటర్ చేయండి!'
                        )
                      else:
                        st.success(
                            f'✅ {m_name} యొక్క PMJJBY వివరాలు విజయవంతంగా సేవ్'
                            ' చేయబడ్డాయి!'
                        )
                        st.rerun()  # సేవ్ అయిన వెంటనే ఆటోమేటిక్‌గా క్లోజ్/రిఫ్రెష్ అవ్వడానికి
                    else:  # Not Enrolled
                      if pmjjby_sub_date is None and pmjjby_b_date is None:
                        st.error(
                            '⚠️ దయచేసి "అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ"'
                            ' లేదా "బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ" లో ఏదో ఒక'
                            ' తేదీని ఎంటర్ చేయండి!'
                        )
                      else:
                        st.success(
                            f'✅ {m_name} యొక్క PMJJBY వివరాలు విజయవంతంగా సేవ్'
                            ' చేయబడ్డాయి!'
                        )
                        st.rerun()  # సేవ్ అయిన వెంటనే ఆటోమేటిక్‌గా క్లోజ్/రిఫ్రెష్ అవ్వడానికి
                  st.markdown('---')
                else:
                  st.warning(
                      'ℹ️ మెంబర్ వయస్సు 50 సంవత్సరాలు దాటడం వలన PMJJBY వర్తించదు'
                      ' (Not Applicable).'
                  )
                  st.markdown('---')

                # ==================== 2. PMSBY Section ====================
                st.markdown('### 📌 2. PMSBY స్కీమ్ వివరాలు (18 నుండి 70 లోపు)')
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

                pmsby_sub_date = None
                pmsby_b_date = None

                if pmsby_enrolled == 'Already Enrolled':
                  pmsby_b_date = st.date_input(
                      'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) -'
                      ' PMSBY',
                      value=None,
                      key=f'pmsby_b_date_already_{idx}',
                  )
                else:
                  col_d3, col_d4 = st.columns(2)
                  with col_d3:
                    pmsby_sub_date = st.date_input(
                        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application'
                        ' Submitted at Bank) - PMSBY',
                        value=None,
                        key=f'pmsby_sub_date_{idx}',
                    )
                  with col_d4:
                    pmsby_b_date = st.date_input(
                        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) -'
                        ' PMSBY',
                        value=None,
                        key=f'pmsby_b_date_opt_{idx}',
                    )

                if st.button(
                    f'💾 {m_name} - PMSBY వివరాలు సేవ్ చేయండి',
                    key=f'save_pmsby_{idx}',
                ):
                  if pmsby_enrolled == 'Already Enrolled':
                    if pmsby_b_date is None:
                      st.error(
                          '⚠️ దయచేసి "బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ" (Bank'
                          ' Enrolled Date) ఎంటర్ చేయండి!'
                      )
                    else:
                      st.success(
                          f'✅ {m_name} యొక్క PMSBY వివరాలు విజయవంతంగా సేవ్'
                          ' చేయబడ్డాయి!'
                      )
                      st.rerun()  # సేవ్ అయిన వెంటనే ఆటోమేటిక్‌గా క్లోజ్/రిఫ్రెష్ అవ్వడానికి
                  else:  # Not Enrolled
                    if pmsby_sub_date is None and pmsby_b_date is None:
                      st.error(
                          '⚠️ దయచేసి "అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ"'
                          ' లేదా "బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ" లో ఏదో ఒక తేదీని'
                          ' ఎంటర్ చేయండి!'
                      )
                    else:
                      st.success(
                          f'✅ {m_name} యొక్క PMSBY వివరాలు విజయవంతంగా సేవ్'
                          ' చేయబడ్డాయి!'
                      )
                      st.rerun()  # సేవ్ అయిన వెంటనే ఆటోమేటిక్‌గా క్లోజ్/రిఫ్రెష్ అవ్వడానికి

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

    temp_df['PMJJBY_Eligible'] = temp_df['AGE'].apply(
        lambda x: 1 if 18 <= x <= 50 else 0
    )
    temp_df['PMSBY_Eligible'] = temp_df['AGE'].apply(
        lambda x: 1 if 18 <= x <= 70 else 0
    )

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
