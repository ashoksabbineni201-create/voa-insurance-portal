from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS - Button colors kosam
st.markdown("""
    <style>
    /* 1. Confirm Age Button (Blue / Primary) */
    div[data-testid="stButton"] > button[kind="primary"] {
        background-color: #1E88E5 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background-color: #1565C0 !important;
    }

    /* 2. Save All Button (Green / Success) */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #2E7D32 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        border: 1px solid #2E7D32 !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #1B5E20 !important;
        color: white !important;
        border-color: #1B5E20 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Google Sheet link
sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url, dtype=str) # Column data types sync kosam string ga load chestunnam
        df.columns = df.columns.str.strip()
        if 'MANDAL' in df.columns:
            df['MANDAL'] = df['MANDAL'].astype(str).str.strip().str.title()
        return df
    except Exception as e:
        st.error(f'Data load avvadamlo lopam jarigindi: {e}')
        return None


df = load_data()

if df is not None:
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
            df[c] = None

    if 'saved_entries_dict' not in st.session_state:
        st.session_state.saved_entries_dict = {}

    st.sidebar.header('📁 నావిగేషన్')
    st.sidebar.markdown('---')
    st.sidebar.markdown('### 📥 రిపోర్ట్ డౌన్‌లోడ్')

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

    report_df = export_df_base[
        export_df_base[col_pmjjby_sub].notna()
        | export_df_base[col_pmjjby_bank].notna()
        | export_df_base[col_pmsby_sub].notna()
        | export_df_base[col_pmsby_bank].notna()
    ]

    export_df = report_df.copy()
    rename_dict = {}
    if col_pmjjby_sub in export_df.columns:
        rename_dict[col_pmjjby_sub] = 'Application Submitted at Bank - PMJJBY'
    if col_pmsby_sub in export_df.columns:
        rename_dict[col_pmsby_sub] = 'Application Submitted at Bank - PMSBY'
    if col_pmjjby_bank in export_df.columns:
        rename_dict[col_pmjjby_bank] = 'Bank Enrolled Date - PMJJBY'
    if col_pmsby_bank in export_df.columns:
        rename_dict[col_pmsby_bank] = 'Bank Enrolled Date - PMSBY'

    export_df = export_df.rename(columns=rename_dict)

    if 's.no' not in export_df.columns and not export_df.empty:
        export_df.insert(0, 's.no', range(1, len(export_df) + 1))
    if 'AGE' in export_df.columns:
        export_df['age correction'] = export_df['AGE']

    desired_columns = [
        's.no',
        'MANDAL',
        'VO',
        'SHG',
        'MEMBER NAME',
        'MEMBER ID',
        'AGE',
        'BANK NAME',
        'BRANCH NAME',
        'MEMBER SB ACCOUNT NUMBER',
        'Application Submitted at Bank - PMJJBY',
        'Bank Enrolled Date - PMJJBY',
        'Application Submitted at Bank - PMSBY',
        'Bank Enrolled Date - PMSBY',
        'age correction',
    ]

    final_columns = [c for c in desired_columns if c in export_df.columns]
    export_df = export_df[final_columns]

    entered_csv_report = export_df.to_csv(index=False).encode('utf-8-sig')
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
                        ' bold; font-size: 20px;">🔑 VOA & SHG Insurance Enrollment Portal</div>',
                        unsafe_allow_html=True,
                    )
                    st.write('---')

                    st.markdown('### 👥 SHG Sabhyula Jabhita (Dashboard)')

                    for idx, row in members_df.reset_index().iterrows():
                        m_name = str(row.get('MEMBER NAME', 'Unknown'))
                        m_id = str(row.get('MEMBER ID', f'ID-{idx+1}'))

                        current_row = st.session_state.saved_entries_dict.get(m_id, row)

                        raw_age = current_row.get('AGE', 35)
                        try:
                            raw_age = int(float(raw_age))
                        except Exception:
                            raw_age = 35

                        status_texts = []
                        if pd.notna(current_row.get(col_pmjjby_bank)):
                            status_texts.append('PMJJBY: Enrolled')
                        elif pd.notna(current_row.get(col_pmjjby_sub)):
                            status_texts.append('PMJJBY: Submitted')

                        if pd.notna(current_row.get(col_pmsby_bank)):
                            status_texts.append('PMSBY: Enrolled')
                        elif pd.notna(current_row.get(col_pmsby_sub)):
                            status_texts.append('PMSBY: Submitted')

                        status_badge = ' | '.join(status_texts) if status_texts else "ఎంట్రీ పెండింగ్"

                        with st.expander(
                            f'✏️ {m_name} (ID: {m_id}) | వయస్సు: {raw_age} | Status: {status_badge}'
                        ):
                            entered_age = st.number_input(
                                'మెంబర్ వయస్సు నిర్ధారించండి / మార్చండి (Age - As per Aadhaar):',
                                min_value=1,
                                max_value=100,
                                value=raw_age,
                                key=f'age_{idx}',
                            )

                            age_confirmed = st.button(
                                f'✔️ {m_name} వయస్సును నిర్ధారించండి',
                                key=f'confirm_age_btn_{idx}',
                                type='primary',
                            )

                            session_key = f'confirmed_age_val_{idx}'
                            is_confirmed_key = f'is_age_confirmed_{idx}'

                            if age_confirmed:
                                st.session_state[session_key] = entered_age
                                st.session_state[is_confirmed_key] = True

                            # Vayassu nirdharinchina tarvata matrame form kanipistundi
                            if st.session_state.get(is_confirmed_key, False):
                                active_age = st.session_state.get(session_key, raw_age)

                                st.info(
                                    f'📌 ప్రస్తుతం పరిగణించబడిన వయస్సు: **{active_age} సంవత్సరాలు**'
                                )

                                if active_age < 18:
                                    st.error(
                                        '❌ హెచ్చరిక: మెంబర్ వయస్సు 18 సంవత్సరాల కంటే తక్కువగా ఉంది.'
                                    )
                                elif active_age > 70:
                                    st.error('❌ హెచ్చరిక: మెంబర్ వయస్సు 70 సంవత్సరాలు దాటింది.')
                                else:
                                    st.success('✅ వయస్సు నిబంధనలకు అనుగుణంగా ఉంది.')

                                    pmjjby_sub_date = None
                                    pmjjby_b_date = None
                                    pmjjby_enrolled = 'Not Enrolled'

                                    pmsby_sub_date = None
                                    pmsby_b_date_pmsby = None
                                    pmsby_enrolled = 'Not Enrolled'

                                    # ================= 1. PMJJBY SECTION (18-50) =================
                                    if 18 <= active_age <= 50:
                                        st.markdown('### 📌 1. PMJJBY స్కీమ్ వివరాలు (18 నుండి 50 లోపు)')
                                        bc1, bc2, bc3 = st.columns(3)
                                        with bc1:
                                            st.text_input(
                                                'బ్యాంక్ పేరు (PMJJBY Bank)',
                                                value=str(row.get('BANK NAME', 'Indian Overseas Bank')),
                                                key=f'pmjjby_bank_{idx}',
                                            )
                                        with bc2:
                                            st.text_input(
                                                'బ్రాంచ్ (PMJJBY Branch)',
                                                value=str(row.get('BRANCH NAME', 'VEJENDLA')),
                                                key=f'pmjjby_branch_{idx}',
                                            )
                                        with bc3:
                                            st.text_input(
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
                                            pmjjby_b_date = st.date_input(
                                                'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY',
                                                value=None,
                                                key=f'pmjjby_b_date_already_{idx}',
                                            )
                                        else:
                                            col_d1, col_d2 = st.columns(2)
                                            with col_d1:
                                                pmjjby_sub_date = st.date_input(
                                                    'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMJJBY',
                                                    value=None,
                                                    key=f'pmjjby_sub_date_{idx}',
                                                )
                                            with col_d2:
                                                pmjjby_b_date = st.date_input(
                                                    'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY',
                                                    value=None,
                                                    key=f'pmjjby_b_date_opt_{idx}',
                                                )
                                        st.markdown('---')
                                    else:
                                        st.warning('ℹ️ మెంబర్ వయస్సు 50 సంవత్సరాలు దాటడం వలన PMJJBY వర్తించదు.')
                                        st.markdown('---')

                                    # ================= 2. PMSBY SECTION (18-70) =================
                                    if 18 <= active_age <= 70:
                                        st.markdown('### 📌 2. PMSBY స్కీమ్ వివరాలు (18 నుండి 70 లోపు)')
                                        pc1, pc2, pc3 = st.columns(3)
                                        with pc1:
                                            st.text_input(
                                                'బ్యాంక్ పేరు (PMSBY Bank)',
                                                value=str(row.get('BANK NAME', 'Indian Overseas Bank')),
                                                key=f'pmsby_bank_{idx}',
                                            )
                                        with pc2:
                                            st.text_input(
                                                'బ్రాంచ్ (PMSBY Branch)',
                                                value=str(row.get('BRANCH NAME', 'VEJENDLA')),
                                                key=f'pmsby_branch_{idx}',
                                            )
                                        with pc3:
                                            st.text_input(
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
                                            pmsby_b_date_pmsby = st.date_input(
                                                'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMSBY',
                                                value=None,
                                                key=f'pmsby_b_date_already_{idx}',
                                            )
                                        else:
                                            col_d3, col_d4 = st.columns(2)
                                            with col_d3:
                                                pmsby_sub_date = st.date_input(
                                                    'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMSBY',
                                                    value=None,
                                                    key=f'pmsby_sub_date_{idx}',
                                                )
                                            with col_d4:
                                                pmsby_b_date_pmsby = st.date_input(
                                                    'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMSBY',
                                                    value=None,
                                                    key=f'pmsby_b_date_opt_{idx}',
                                                )
                                        st.markdown('---')

                                    # ================= SAVE BUTTON =================
                                    save_btn = st.button(
                                        f'💾 {m_name} - అన్ని వివరాలు సేవ్ చేయండి (Save All)',
                                        key=f'save_all_{idx}',
                                        type='secondary',
                                    )

                                    if save_btn:
                                        has_entered_any_date = (
                                            (pmjjby_sub_date is not None) or
                                            (pmjjby_b_date is not None) or
                                            (pmsby_sub_date is not None) or
                                            (pmsby_b_date_pmsby is not None)
                                        )

                                        if not has_entered_any_date:
                                            st.error('❌ దయచేసి వివరాలు సేవ్ చేయడానికి PMJJBY లేదా PMSBY లో కనీసం ఒక తేదీని నమోదు చేయండి!')
                                        else:
                                            updated_row = row.to_dict()
                                            updated_row['AGE'] = str(active_age)
                                            updated_row['age correction'] = str(active_age)

                                            # Save PMJJBY Data
                                            if active_age <= 50:
                                                if pmjjby_enrolled == 'Already Enrolled':
                                                    if pmjjby_b_date is not None:
                                                        updated_row[col_pmjjby_bank] = str(pmjjby_b_date)
                                                else:
                                                    if pmjjby_sub_date is not None:
                                                        updated_row[col_pmjjby_sub] = str(pmjjby_sub_date)
                                                    if pmjjby_b_date is not None:
                                                        updated_row[col_pmjjby_bank] = str(pmjjby_b_date)

                                            # Save PMSBY Data
                                            if active_age <= 70:
                                                if pmsby_enrolled == 'Already Enrolled':
                                                    if pmsby_b_date_pmsby is not None:
                                                        updated_row[col_pmsby_bank] = str(pmsby_b_date_pmsby)
                                                else:
                                                    if pmsby_sub_date is not None:
                                                        updated_row[col_pmsby_sub] = str(pmsby_sub_date)
                                                    if pmsby_b_date_pmsby is not None:
                                                        updated_row[col_pmsby_bank] = str(pmsby_b_date_pmsby)

                                            st.session_state.saved_entries_dict[m_id] = updated_row
                                            st.success(
                                                f'✅ {m_name} యొక్క అన్ని వివరాలు విజయవంతంగా సేవ్ చేయబడ్డాయి!'
                                            )
                                            st.toast(
                                                f'✅ {m_name} - All Details Saved Successfully!',
                                                icon='🎉',
                                            )
                                            st.rerun()
                            else:
                                st.warning('⚠️ దయచేసి వివరాలు నమోదు చేయడానికి ముందు "వయస్సును నిర్ధారించండి" బటన్ నొక్కండి.')

    elif app_mode == '📊 జిల్లా అబ్‌స్ట్రాక్ట్ & రిపోర్ట్':
        st.markdown('## 📊 మండలాల వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్ (Abstract Summary)')
        st.write(
            'ఇక్కడ జిల్లాలోని అన్ని మండలాల వారీగా PMJJBY (18-50) మరియు PMSBY (18-70)'
            ' ఎలిజిబిలిటీ టార్గెట్, బ్యాంక్ సబ్మిటెడ్, బ్యాంక్ ఎన్‌రోల్డ్ మరియు'
            ' బ్యాలెన్స్ వివరాల అబ్‌స్ట్రాక్ట్ టేబుల్ కింద గ్రాండ్ టోటల్‌తో సహా కనిపిస్తుంది.'
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
                PMSBY_Submitted_Bank=('PMSBY_Submitted_Bank', 'sum'),
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
            f'📋 Mandal-wise Abstract Summary with Grand Total (Total Mandals: {len(abstract_df)-1})'
        )
        st.dataframe(abstract_df, use_container_width=True)

        csv_data = abstract_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=(
                '📥 అబ్‌స్ట్రాక్ట్ గ్రాండ్ టోటల్ రిపోర్ట్‌ని CSV రూపంలో డౌన్‌లోడ్ చేసుకోండి'
            ),
            data=csv_data,
            file_name='District_Insurance_Abstract_With_Total.csv',
            mime='text/csv',
        )
