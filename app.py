from datetime import date
import io
import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title='Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS: Green & Amber Theme, No Blue tones, Custom styled Save buttons
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
    .section-title-pmjjby {
        color: #15803d;
        background: #f0fdf4;
        border-left: 5px solid #15803d;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
        margin-bottom: 15px;
        font-weight: 700;
        font-size: 18px;
    }
    .section-title-pmsby {
        color: #b45309;
        background: #fef3c7;
        border-left: 5px solid #b45309;
        padding: 10px 15px;
        border-radius: 0 8px 8px 0;
        margin-top: 20px;
        margin-bottom: 15px;
        font-weight: 700;
        font-size: 18px;
    }
    div.stAlert {
        background-color: #fefce8 !important;
        color: #854d0e !important;
        border: 1px solid #fef08a !important;
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


with st.spinner(
    'దయచేసి వేచి ఉండండి, డేటా లోడ్ చేయబడుతోంది...'
):
    df = load_data()

if df is None:
    st.error(
        '❌ డేటా లోడ్ అవ్వడంలో సమస్య ఏర్పడింది. దయచేసి పేజీని రిఫ్రెష్ (Refresh)'
        ' చేయండి.'
    )
else:
    col_pmjjby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMJJBY'
    )
    col_pmjjby_bank = (
        'బ్యాంకు వారు ఎన్‌‌‌‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY'
    )
    col_pmsby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMSBY'
    )
    col_pmsby_bank = (
        'బ్యాంకు వారు ఎన్రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMSBY'
    )
    col_corrected_name = 'AADHAAR CORRECTED NAME'
    col_original_name = 'ORIGINAL MEMBER NAME'
    col_original_age = 'ORIGINAL AGE'

    for c in [
        col_pmjjby_sub,
        col_pmjjby_bank,
        col_pmsby_sub,
        col_pmsby_bank,
        col_corrected_name,
        col_original_name,
        col_original_age,
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
                    export_df_base.loc[idx_match, k] = (
                        str(v) if v is not None else None
                    )

    # Backup original names & ages if not set
    for idx, r in export_df_base.iterrows():
        if pd.isna(r.get(col_original_name)) or not r.get(col_original_name):
            export_df_base.loc[idx, col_original_name] = r.get('MEMBER NAME', '')
        if pd.isna(r.get(col_original_age)) or not r.get(col_original_age):
            export_df_base.loc[idx, col_original_age] = r.get('AGE', '')

    export_df_base['NUM_AGE'] = pd.to_numeric(
        export_df_base['AGE'], errors='coerce'
    ).fillna(0)

    # Header Title
    st.markdown(
        '<div class="portal-header"><h1>గుంటూరు జిల్లా - SHG సభ్యుల బీమా (PMJJBY & PMSBY) ఎన్‌రోల్‌మెంట్ పోర్టల్</h1><p>సంఘ సభ్యులందరికీ సులభంగా ఇన్సూరెన్స్ నమోదు మరియు ట్రాకింగ్ చేయు విధానం</p></div>',
        unsafe_allow_html=True,
    )

    # Top Mobile-Friendly Navigation Selector
    nav_options_mapping = {
        '1️⃣ 🏠 డాష్‌‌బోర్డ్ (Dashboard & Entry)': 'Dashboard',
        '2️⃣ 📍 మండలం వారీగా రిపోర్ట్ (Mandal Wise)': 'Mandal Wise',
        '3️⃣ 📊 వి.ఓ (VO) వారీగా రిపోర్ట్ (VO Wise)': 'VO Wise',
        '4️⃣ 🏛️ బ్యాంక్ వారీగా రిపోర్ట్ (Bank Wise)': 'Bank Wise',
        '5️⃣ 📈 బ్రాంచ్ వారీగా రిపోర్ట్ (Branch Wise)': 'Branch Wise',
        '6️⃣ 📥 పెండింగ్ జాబితా (Pending Reports)': 'Pending Reports',
        '7️⃣ 👥 పూర్తి సభ్యుల జాబితా (Member Level)': 'Member Level',
        '8️⃣ 📝 పేరు కరెక్షన్ నివేదిక (Name Corrections)': 'Name Corrections',
        '9️⃣ 🔢 వయస్సు కరెక్షన్ నివేదిక (Age Corrections)': 'Age Corrections',
    }

    selected_display_opt = st.selectbox(
        '📌 దయచేసి క్రింది మెను నుండి కావలసిన సెక్షన్ లేదా రిపోర్ట్ ఎంచుకోండి:',
        list(nav_options_mapping.keys()),
        key='mobile_friendly_main_nav',
    )

    app_mode = nav_options_mapping[selected_display_opt]
    st.markdown('---')

    # PAGE 1: DASHBOARD
    if app_mode == 'Dashboard':
        mandals = ['-- ఎంచుకోండి --'] + sorted(
            export_df_base['MANDAL'].dropna().unique().tolist()
        )
        selected_mandal = st.selectbox(
            '1. మండలం ఎంచుకోండి (Select Mandal):', mandals
        )

        selected_vo = None
        selected_shg = None

        if selected_mandal and selected_mandal != '-- ఎంచుకోండి --':
            filtered_vos = ['-- ఎంచుకోండి --'] + sorted(
                export_df_base[export_df_base['MANDAL'] == selected_mandal]['VO']
                .dropna()
                .unique()
                .tolist()
            )
            selected_vo = st.selectbox(
                '2. VO (Village Organization) పేరు ఎంచుకోండి:', filtered_vos
            )

            if selected_vo and selected_vo != '-- ఎంచుకోండి --':
                filtered_shgs = ['-- ఎంచుకోండి --'] + sorted(
                    export_df_base[
                        (export_df_base['MANDAL'] == selected_mandal)
                        & (export_df_base['VO'] == selected_vo)
                    ]['SHG']
                    .dropna()
                    .unique()
                    .tolist()
                )
                selected_shg = st.selectbox(
                    '3. SHG గ్రూప్ ఎంచుకోండి:', filtered_shgs
                )

        if not selected_shg or selected_shg == '-- ఎంచుకోండి --':
            st.info(
                '👉 దయచేసి పైన ఇవ్వబడిన **మండలం, VO మరియు SHG గ్రూప్ను** వరుసగా'
                ' ఎంచుకోండి.'
            )
        else:
            st.markdown(
                f'### 📄 SHG సభ్యుల జాబితా: <span style="color:'
                f' #15803d;">{selected_shg}</span>',
                unsafe_allow_html=True,
            )
            members_df = export_df_base[
                (export_df_base['MANDAL'] == selected_mandal)
                & (export_df_base['VO'] == selected_vo)
                & (export_df_base['SHG'] == selected_shg)
            ]

            for idx, row in members_df.reset_index(drop=True).iterrows():
                m_id = str(row.get('MEMBER ID', f'ID-{idx+1}'))
                current_row = st.session_state.saved_entries_dict.get(
                    m_id, row
                )

                orig_name = str(row.get('MEMBER NAME', 'Unknown'))
                corr_name_val = current_row.get(col_corrected_name)
                display_name = (
                    str(corr_name_val)
                    if pd.notna(corr_name_val)
                    and str(corr_name_val).strip() != ''
                    else orig_name
                )

                raw_age = current_row.get('AGE', 35)
                try:
                    raw_age = int(float(raw_age))
                except Exception:
                    raw_age = 35

                p_sub = current_row.get(col_pmjjby_sub)
                p_bank = current_row.get(col_pmjjby_bank)
                s_sub = current_row.get(col_pmsby_sub)
                s_bank = current_row.get(col_pmsby_bank)

                status_tags = []
                if raw_age > 70:
                    status_tags.append('❌ Not Eligible')
                else:
                    if (
                        pd.notna(p_bank)
                        and str(p_bank).lower() != 'nan'
                        and str(p_bank).strip() != ''
                    ):
                        status_tags.append('🛡️ PMJJBY Enrolled')
                    elif (
                        pd.notna(p_sub)
                        and str(p_sub).lower() != 'nan'
                        and str(p_sub).strip() != ''
                    ):
                        status_tags.append('🛡️ PMJJBY App Submitted')

                    if (
                        pd.notna(s_bank)
                        and str(s_bank).lower() != 'nan'
                        and str(s_bank).strip() != ''
                    ):
                        status_tags.append('🚑 PMSBY Enrolled')
                    elif (
                        pd.notna(s_sub)
                        and str(s_sub).lower() != 'nan'
                        and str(s_sub).strip() != ''
                    ):
                        status_tags.append('🚑 PMSBY App Submitted')

                    if not status_tags:
                        status_tags.append('⏳ పెండింగ్ (Pending)')

                status_str = ' | '.join(status_tags)

                is_already_saved = m_id in st.session_state.saved_entries_dict or (
                    pd.notna(current_row.get(col_pmjjby_sub))
                    or pd.notna(current_row.get(col_pmjjby_bank))
                    or pd.notna(current_row.get(col_pmsby_sub))
                    or pd.notna(current_row.get(col_pmsby_bank))
                    or pd.notna(current_row.get(col_corrected_name))
                )

                with st.expander(
                    f'👤 {display_name} | వయస్సు: {raw_age} -- [{status_str}]'
                ):

                    st.markdown(
                        '##### 📝 ఆధార్ ప్రకారం పేరు నిర్ధారణ (Aadhaar Name'
                        ' Verification):'
                    )
                    name_status_key = f'name_status_{idx}'

                    if name_status_key not in st.session_state:
                        if (
                            pd.notna(current_row.get(col_corrected_name))
                            and str(
                                current_row.get(col_corrected_name)
                            ).strip()
                            != ''
                        ):
                            st.session_state[name_status_key] = 'No (కలదు)'
                        else:
                            st.session_state[name_status_key] = (
                                'Yes (సరిగ్గా ఉంది)'
                            )

                    name_check_opt = st.radio(
                        f'"{orig_name}" పేరు ఆధార్ కార్డు ప్రకారం సరిగ్గా ఉందా?',
                        ['Yes (సరిగ్గా ఉంది)', 'No (కరెక్షన్ చేయాలి)'],
                        key=f'name_radio_{idx}',
                    )

                    final_corrected_name = orig_name
                    if 'No' in name_check_opt:
                        final_corrected_name = st.text_input(
                            'దయచేసి ఆధార్ ప్రకారం సరైన పేరు నమోదు చేయండి'
                            ' (Corrected Name):',
                            value=str(
                                current_row.get(
                                    col_corrected_name, orig_name
                                )
                            ),
                            key=f'input_corr_name_{idx}',
                        )
                        st.info(
                            f'📌 **పాత పేరు:** {orig_name} | **కొత్త పేరు:**'
                            f' {final_corrected_name}'
                        )

                    st.markdown('---')

                    is_age_confirmed_key = f'is_age_confirmed_{idx}'
                    if is_already_saved:
                        st.session_state[is_age_confirmed_key] = True

                    if not st.session_state.get(is_age_confirmed_key, False):
                        entered_age = st.number_input(
                            'మెంబర్ వయస్సు నిర్ధారించండి / మార్చండి (Age):',
                            min_value=1,
                            max_value=100,
                            value=raw_age,
                            key=f'age_{idx}',
                        )

                        age_confirmed_btn = st.button(
                            f'✔️ వయస్సును నిర్ధారించండి',
                            key=f'confirm_age_btn_{idx}',
                            type='primary',
                        )

                        if age_confirmed_btn:
                            st.session_state[
                                f'confirmed_age_val_{idx}'
                            ] = entered_age
                            st.session_state[is_age_confirmed_key] = True
                            st.rerun()

                    if st.session_state.get(is_age_confirmed_key, False):
                        active_age = st.session_state.get(
                            f'confirmed_age_val_{idx}', raw_age
                        )

                        if active_age > 70:
                            st.error(
                                '❌ ఈ సభ్యురాలు 70 సంవత్సరాలు దాటినందున'
                                ' బీమా పథకాలకు అర్హులు కాదు (Not Eligible).'
                            )
                        else:
                            pmjjby_sub_date, pmjjby_b_date = None, None
                            pmsby_sub_date, pmsby_b_date_pmsby = None, None

                            def safe_parse_date(val):
                                if (
                                    pd.isna(val)
                                    or not val
                                    or str(val).lower() == 'nan'
                                ):
                                    return None
                                try:
                                    return pd.to_datetime(val).date()
                                except:
                                    return None

                            existing_pm_sub = safe_parse_date(
                                current_row.get(col_pmjjby_sub)
                            )
                            existing_pm_bank = safe_parse_date(
                                current_row.get(col_pmjjby_bank)
                            )
                            existing_ps_sub = safe_parse_date(
                                current_row.get(col_pmsby_sub)
                            )
                            existing_ps_bank = safe_parse_date(
                                current_row.get(col_pmsby_bank)
                            )

                            if 18 <= active_age <= 50:
                                st.markdown(
                                    '<div'
                                    ' class="section-title-pmjjby">🛡 1.'
                                    ' PMJJBY స్కీమ్ వివరాలు (18-50'
                                    ' సంవత్సరాలు)</div>',
                                    unsafe_allow_html=True,
                                )
                                bc1, bc2, bc3 = st.columns(3)
                                with bc1:
                                    st.text_input(
                                        'PMJJBY Bank',
                                        value=str(row.get('BANK NAME', '')),
                                        key=f'pmjjby_bank_{idx}',
                                    )
                                with bc2:
                                    st.text_input(
                                        'PMJJBY Branch',
                                        value=str(row.get('BRANCH NAME', '')),
                                        key=f'pmjjby_branch_{idx}',
                                    )
                                with bc3:
                                    st.text_input(
                                        'PMJJBY Acc No',
                                        value=str(
                                            row.get(
                                                'MEMBER SB ACCOUNT NUMBER', ''
                                            )
                                        ),
                                        key=f'pmjjby_acc_{idx}',
                                    )

                                col_d1, col_d2 = st.columns(2)
                                with col_d1:
                                    pmjjby_sub_date = st.date_input(
                                        'Application Submitted Date - PMJJBY'
                                        ' (అప్లికేషన్ తేదీ ఇవ్వాలి)',
                                        value=existing_pm_sub,
                                        key=f'pmjjby_sub_{idx}',
                                    )
                                with col_d2:
                                    pmjjby_b_date = st.date_input(
                                        'Bank Enrolled Date - PMJJBY',
                                        value=existing_pm_bank,
                                        key=f'pmjjby_b_opt_{idx}',
                                    )

                            if 18 <= active_age <= 70:
                                st.markdown(
                                    '<div'
                                    ' class="section-title-pmsby">🚑 2.'
                                    ' PMSBY స్కీమ్ వివరాలు (18-70'
                                    ' సంవత్సరాలు)</div>',
                                    unsafe_allow_html=True,
                                )
                                pc1, pc2, pc3 = st.columns(3)
                                with pc1:
                                    st.text_input(
                                        'PMSBY Bank',
                                        value=str(row.get('BANK NAME', '')),
                                        key=f'pmsby_bank_{idx}',
                                    )
                                with pc2:
                                    st.text_input(
                                        'PMSBY Branch',
                                        value=str(row.get('BRANCH NAME', '')),
                                        key=f'pmsby_branch_{idx}',
                                    )
                                with pc3:
                                    st.text_input(
                                        'PMSBY Acc No',
                                        value=str(
                                            row.get(
                                                'MEMBER SB ACCOUNT NUMBER', ''
                                            )
                                        ),
                                        key=f'pmsby_acc_{idx}',
                                    )

                                col_d3, col_d4 = st.columns(2)
                                with col_d3:
                                    pmsby_sub_date = st.date_input(
                                        'Application Submitted Date - PMSBY'
                                        ' (అప్లికేషన్ తేదీ ఇవ్వాలి)',
                                        value=existing_ps_sub,
                                        key=f'pmsby_sub_{idx}',
                                    )
                                with col_d4:
                                    pmsby_b_date_pmsby = st.date_input(
                                        'Bank Enrolled Date - PMSBY',
                                        value=existing_ps_bank,
                                        key=f'pmsby_b_opt_{idx}',
                                    )

                            if st.button(
                                f'💾 {display_name} వివరాలు సేవ్ చేయండి',
                                key=f'save_{idx}',
                                type='primary',
                            ):
                                date_error = False

                                if pmjjby_b_date and not pmjjby_sub_date:
                                    date_error = True
                                    st.error(
                                        '❌ PMJJBY లో: ముందుగా అప్లికేషన్'
                                        ' బ్యాంకుకు సబ్మిట్ చేసిన తేదీ'
                                        ' ఇవ్వకుండా, నేరుగా బ్యాంకు ఎన్‌‌రోల్'
                                        ' చేసిన తేదీ ఇవ్వకూడదు!'
                                    )

                                if (
                                    pmsby_b_date_pmsby
                                    and not pmsby_sub_date
                                ):
                                    date_error = True
                                    st.error(
                                        '❌ PMSBY లో: ముందుగా అప్లికేషన్'
                                        ' బ్యాంకుకు సబ్మిట్ చేసిన తేదీ'
                                        ' ఇవ్వకుండా, నేరుగా బ్యాంకు ఎన్‌‌‌రోల్'
                                        ' చేసిన తేదీ ఇవ్వకూడదు!'
                                    )

                                if (
                                    not date_error
                                    and pmjjby_sub_date
                                    and pmjjby_b_date
                                ):
                                    if pmjjby_b_date < pmjjby_sub_date:
                                        date_error = True
                                        st.error(
                                            '❌ PMJJBY లో: బ్యాంకు ఎన్‌రోల్'
                                            ' చేసిన తేదీ, అప్లికేషన్ సబ్మిట్'
                                            ' చేసిన తేదీ కంటే ముందు ఉండకూడదు!'
                                        )

                                if (
                                    not date_error
                                    and pmsby_sub_date
                                    and pmsby_b_date_pmsby
                                ):
                                    if pmsby_b_date_pmsby < pmsby_sub_date:
                                        date_error = True
                                        st.error(
                                            '❌ PMSBY లో: బ్యాంకు ఎన్‌రోల్'
                                            ' చేసిన తేదీ, అప్లికేషన్ సబ్మిట్'
                                            ' చేసిన తేదీ కంటే ముందు ఉండకూడదు!'
                                        )

                                if not date_error:
                                    updated_row = row.to_dict()
                                    updated_row['AGE'] = str(active_age)
                                    updated_row[col_original_name] = orig_name
                                    updated_row[col_original_age] = str(
                                        row.get('AGE', '')
                                    )

                                    if 'No' in name_check_opt:
                                        updated_row[col_corrected_name] = (
                                            str(final_corrected_name).strip()
                                        )
                                    else:
                                        updated_row[col_corrected_name] = None

                                    if pmjjby_sub_date:
                                        updated_row[col_pmjjby_sub] = str(
                                            pmjjby_sub_date
                                        )
                                    if pmjjby_b_date:
                                        updated_row[col_pmjjby_bank] = str(
                                            pmjjby_b_date
                                        )
                                    if pmsby_sub_date:
                                        updated_row[col_pmsby_sub] = str(
                                            pmsby_sub_date
                                        )
                                    if pmsby_b_date_pmsby:
                                        updated_row[col_pmsby_bank] = str(
                                            pmsby_b_date_pmsby
                                        )

                                    st.session_state.saved_entries_dict[
                                        m_id
                                    ] = updated_row
                                    st.success(
                                        '✅ వివరాలు విజయవంతంగా సేవ్ చేయబడ్డాయి!'
                                    )
                                    st.rerun()

    # 2. MANDAL WISE
    elif app_mode == 'Mandal Wise':
        st.markdown('## 📍 మండలం వారీగా సారాంశం (Mandal Wise)')
        st.write('---')
        scheme_choice = st.radio(
            'స్కీమ్‌‌ను ఎంచుకోండి:',
            ['🛡️ PMJJBY', '🚑 PMSBY'],
            horizontal=True,
            key='m_scheme',
        )

        mandal_summary = []
        for m_name, group in export_df_base.groupby('MANDAL'):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmjjby_sub].notna()
                    & elig[col_pmjjby_bank].isna()
                ].shape[0]
            else:
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmsby_sub].notna()
                    & elig[col_pmsby_bank].isna()
                ].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)

            mandal_summary.append({
                'Mandal Name': m_name,
                'Target': target,
                'Enrolled': enrolled,
                'Balance': balance,
                'Applications Submitted': submitted,
                'Yet to Submit': yet_to_submit,
            })
        st.dataframe(pd.DataFrame(mandal_summary), use_container_width=True)

    # 3. VO WISE
    elif app_mode == 'VO Wise':
        st.markdown('## 📊 వి.ఓ (VO) వారీగా సారాంశం')
        st.write('---')
        mandals_list = ['అన్నీ (All Mandals)'] + sorted(
            export_df_base['MANDAL'].dropna().unique().tolist()
        )
        selected_mandal_filter = st.selectbox(
            'మండలం ఎంచుకోండి:', mandals_list
        )
        scheme_choice = st.radio(
            'స్కీమ్‌ను ఎంచుకోండి:',
            ['🛡️ PMJJBY', '🚑 PMSBY'],
            horizontal=True,
            key='vo_scheme',
        )

        filtered_df = export_df_base.copy()
        if selected_mandal_filter != 'అన్నీ (All Mandals)':
            filtered_df = filtered_df[
                filtered_df['MANDAL'] == selected_mandal_filter
            ]

        vo_summary = []
        for (mandal, vo), group in filtered_df.groupby(['MANDAL', 'VO']):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmjjby_sub].notna()
                    & elig[col_pmjjby_bank].isna()
                ].shape[0]
            else:
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmsby_sub].notna()
                    & elig[col_pmsby_bank].isna()
                ].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)
            vo_summary.append({
                'Mandal Name': mandal,
                'VO Name': vo,
                'Target': target,
                'Enrolled': enrolled,
                'Balance': balance,
                'Applications Submitted': submitted,
                'Yet to Submit': yet_to_submit,
            })

        st.dataframe(pd.DataFrame(vo_summary), use_container_width=True)

    # 4. BANK WISE
    elif app_mode == 'Bank Wise':
        st.markdown('## 🏛️ బ్యాంక్ వారీగా సారాంశం')
        st.write('---')
        scheme_choice = st.radio(
            'స్కీమ్‌ను ఎంచుకోండి:',
            ['🛡️ PMJJBY', '🚑 PMSBY'],
            horizontal=True,
            key='bank_wise_scheme',
        )

        bank_summary = []
        for bank, group in export_df_base.groupby('BANK NAME'):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmjjby_sub].notna()
                    & elig[col_pmjjby_bank].isna()
                ].shape[0]
            else:
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmsby_sub].notna()
                    & elig[col_pmsby_bank].isna()
                ].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)
            bank_summary.append({
                'Bank Name': bank,
                'Target': target,
                'Enrolled': enrolled,
                'Balance': balance,
                'Applications Submitted': submitted,
                'Yet to Submit': yet_to_submit,
            })

        st.dataframe(pd.DataFrame(bank_summary), use_container_width=True)

    # 5. BRANCH WISE
    elif app_mode == 'Branch Wise':
        st.markdown('## 📈 బ్రాంచ్ వారీగా సారాంశం')
        st.write('---')
        banks_list = ['అన్నీ (All Banks)'] + sorted(
            export_df_base['BANK NAME'].dropna().unique().tolist()
        )
        selected_bank_filter = st.selectbox('బ్యాంక్ ఎంచుకోండి:', banks_list)
        scheme_choice = st.radio(
            'స్కీమ్‌ను ఎంచుకోండి:',
            ['🛡️ PMJJBY', '🚑 PMSBY'],
            horizontal=True,
            key='b_scheme',
        )

        filtered_bank_df = export_df_base.copy()
        if selected_bank_filter != 'అన్నీ (All Banks)':
            filtered_bank_df = filtered_bank_df[
                filtered_bank_df['BANK NAME'] == selected_bank_filter
            ]

        bank_branch_summary = []
        for (bank, branch), group in filtered_bank_df.groupby(
            ['BANK NAME', 'BRANCH NAME']
        ):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmjjby_sub].notna()
                    & elig[col_pmjjby_bank].isna()
                ].shape[0]
            else:
                elig = group[
                    (group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)
                ]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[
                    elig[col_pmsby_sub].notna()
                    & elig[col_pmsby_bank].isna()
                ].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)
            bank_branch_summary.append({
                'Bank Name': bank,
                'Branch Name': branch,
                'Target': target,
                'Enrolled': enrolled,
                'Balance': balance,
                'Applications Submitted': submitted,
                'Yet to Submit': yet_to_submit,
            })

        st.dataframe(pd.DataFrame(bank_branch_summary), use_container_width=True)

    # 6. PENDING LIST
    elif app_mode == 'Pending Reports':
        st.markdown('## 📥 పెండింగ్ మరియు ఎన్‌రోల్‌మెంట్ నివేదికలు')
        st.write('---')
        report_type = st.selectbox(
            'రిపోర్ట్ రకం ఎంచుకోండి:',
            [
                '1. ఇప్పటివరకు ఎన్రోల్ అయినవారు (Completed / Enrolled List)',
                (
                    '2. అప్లికేషన్ బ్యాంకుకు ఇచ్చి, ఎన్రోల్ కానివారు'
                    ' (Submitted & Pending at Bank)'
                ),
                '3. ఇంకా బ్యాంకుకు అప్లికేషన్ ఇవ్వనివారు (Yet to Submit to Bank)',
            ],
        )
        scheme_filter = st.radio(
            'స్కీమ్ ఎంచుకోండి:',
            ['🛡️ PMJJBY', '🚑 PMSBY'],
            horizontal=True,
        )
        is_pmjjby = scheme_filter == '🛡️ PMJJBY'

        area_scope = st.radio(
            'స్థాయి ఎంచుకోండి:',
            ['🌐 జిల్లా అంతా (Entire District)', '📍 నిర్దిష్ట మండలం (Specific Mandal)'],
            horizontal=True,
        )
        target_df = export_df_base.copy()
        if area_scope == '📍 నిర్దిష్ట మండలం (Specific Mandal)':
            mandals_list_det = sorted(
                target_df['MANDAL'].dropna().unique().tolist()
            )
            chosen_mandal = st.selectbox('మండలం ఎంచుకోండి:', mandals_list_det)
            target_df = target_df[target_df['MANDAL'] == chosen_mandal]

        result_list = []
        if '1.' in report_type:
            if is_pmjjby:
                result_list = target_df[
                    (target_df['NUM_AGE'] >= 18)
                    & (target_df['NUM_AGE'] <= 50)
                    & (target_df[col_pmjjby_bank].notna())
                ]
            else:
                result_list = target_df[
                    (target_df['NUM_AGE'] >= 18)
                    & (target_df['NUM_AGE'] <= 70)
                    & (target_df[col_pmsby_bank].notna())
                ]
        elif '2.' in report_type:
            if is_pmjjby:
                result_list = target_df[
                    (target_df['NUM_AGE'] >= 18)
                    & (target_df['NUM_AGE'] <= 50)
                    & (target_df[col_pmjjby_sub].notna())
                    & (target_df[col_pmjjby_bank].isna())
                ]
            else:
                result_list = target_df[
                    (target_df['NUM_AGE'] >= 18)
                    & (target_df['NUM_AGE'] <= 70)
                    & (target_df[col_pmsby_sub].notna())
                    & (target_df[col_pmsby_bank].isna())
                ]
        else:
            if is_pmjjby:
                result_list = target_df[
                    (target_df['NUM_AGE'] >= 18)
                    & (target_df['NUM_AGE'] <= 50)
                    & (target_df[col_pmjjby_sub].isna())
                    & (target_df[col_pmjjby_bank].isna())
                ]
            else:
                result_list = target_df[
                    (target_df['NUM_AGE'] >= 18)
                    & (target_df['NUM_AGE'] <= 70)
                    & (target_df[col_pmsby_sub].isna())
                    & (target_df[col_pmsby_bank].isna())
                ]

        st.markdown(
            f'### 📋 సభ్యుల జాబితా (మొత్తం రికార్డులు: {len(result_list)})'
        )
        if not result_list.empty:
            display_cols = [
                'MANDAL',
                'VO',
                'SHG',
                'MEMBER NAME',
                col_corrected_name,
                'MEMBER ID',
                'AGE',
                'BANK NAME',
                'BRANCH NAME',
                'MEMBER SB ACCOUNT NUMBER',
            ]
            if is_pmjjby:
                display_cols += [col_pmjjby_sub, col_pmjjby_bank]
            else:
                display_cols += [col_pmsby_sub, col_pmsby_bank]

            final_display_df = result_list[
                [c for c in display_cols if c in result_list.columns]
            ]
            st.dataframe(final_display_df, use_container_width=True)

            csv_data = final_display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='📥 ఈ రిపోర్ట్‌ని CSV గా డౌన్లోడ్ చేసుకోండి',
                data=csv_data,
                file_name=(
                    f'Insurance_Report_{report_type[:3]}_{scheme_filter[2:]}.csv'
                ),
                mime='text/css',
                type='primary',
            )
        else:
            st.info(
                '👉 ఈ ఫిల్టర్‌కు సరిపోయే రికార్డులు ఏవీ కనుగొనబడలేదు.'
            )

    # 7. MEMBER LIST
    elif app_mode == 'Member Level':
        st.markdown('## 👥 పూర్తి సభ్యుల జాబితా')
        st.write('---')
        selected_mandal_filter = st.selectbox(
            'మండలం ద్వారా ఫిల్టర్ చేయండి:',
            ['అన్నీ (All)']
            + sorted(export_df_base['MANDAL'].dropna().unique().tolist()),
        )

        filtered_report_df = export_df_base.copy()
        if selected_mandal_filter != 'అన్నీ (All)':
            filtered_report_df = filtered_report_df[
                filtered_report_df['MANDAL'] == selected_mandal_filter
            ]

        st.dataframe(
            filtered_report_df[[
                'MANDAL',
                'VO',
                'SHG',
                'MEMBER NAME',
                col_corrected_name,
                'MEMBER ID',
                'AGE',
                col_pmjjby_sub,
                col_pmjjby_bank,
                col_pmsby_sub,
                col_pmsby_bank,
            ]],
            use_container_width=True,
        )

    # 8. NAME CORRECTIONS REPORT
    elif app_mode == 'Name Corrections':
        st.markdown(
            '## 📝 8. పేరు కరెక్షన్ చేసిన సభ్యుల నివేదిక (Name Corrections'
            ' Report)'
        )
        st.write('---')

        name_corr_df = export_df_base[
            export_df_base[col_corrected_name].notna()
            & (export_df_base[col_corrected_name].str.strip() != '')
            & (
                export_df_base[col_corrected_name]
                != export_df_base[col_original_name]
            )
        ]

        st.markdown(
            f'### 📋 మొత్తం పేరు మార్పులు చేసిన రికార్డులు: {len(name_corr_df)}'
        )
        if not name_corr_df.empty:
            report_cols = [
                'MANDAL',
                'VO',
                'SHG',
                col_original_name,
                col_corrected_name,
                'MEMBER ID',
            ]
            name_report_final = name_corr_df[
                [c for c in report_cols if c in name_corr_df.columns]
            ].rename(columns={
                col_original_name: 'పాత పేరు (Original Name)',
                col_corrected_name: 'కొత్త పేరు (Corrected Name)',
            })
            st.dataframe(name_report_final, use_container_width=True)

            csv_name_data = name_report_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='📥 పేరు కరెక్షన్ రిపోర్ట్‌ని CSV గా డౌన్లోడ్ చేసుకోండి',
                data=csv_name_data,
                file_name='Name_Corrections_Report.csv',
                mime='text/css',
                type='primary',
            )
        else:
            st.info('👉 ఇప్పటివరకు ఎలాంటి పేరు కరెక్షన్లు చేయబడలేదు.')

    # 9. AGE CORRECTIONS REPORT
    elif app_mode == 'Age Corrections':
        st.markdown(
            '## 🔢 9. వయస్సు కరెక్షన్ చేసిన సభ్యుల నివేదిక (Age Corrections'
            ' Report)'
        )
        st.write('---')

        age_corr_df = export_df_base[
            export_df_base[col_original_age].notna()
            & (
                export_df_base['AGE'].astype(str)
                != export_df_base[col_original_age].astype(str)
            )
        ]

        st.markdown(
            f'### 📋 మొత్తం వయస్సు మార్పులు చేసిన రికార్డులు: {len(age_corr_df)}'
        )
        if not age_corr_df.empty:
            report_cols_age = [
                'MANDAL',
                'VO',
                'SHG',
                'MEMBER NAME',
                col_corrected_name,
                col_original_age,
                'AGE',
                'MEMBER ID',
            ]
            age_report_final = age_corr_df[
                [c for c in report_cols_age if c in age_corr_df.columns]
            ].rename(columns={
                col_original_age: 'పాత వయస్సు (Original Age)',
                'AGE': 'కొత్త వయస్సు (Updated Age)',
            })
            st.dataframe(age_report_final, use_container_width=True)

            csv_age_data = age_report_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='📥 వయస్సు కరెక్షన్ రిపోర్ట్‌ని CSV గా డౌన్లోడ్ చేసుకోండి',
                data=csv_age_data,
                file_name='Age_Corrections_Report.csv',
                mime='text/css',
                type='primary',
            )
        else:
            st.info('👉 ఇప్పటివరకు ఎలాంటి వయస్సు మార్పులు చేయబడలేదు.')
