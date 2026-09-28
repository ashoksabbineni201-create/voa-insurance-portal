from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS - App styling
st.markdown("""
    <style>
    /* 1. Main Background & Font Enhancement */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* 2. Top Header Styling */
    .portal-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        color: white !important;
        margin-bottom: 25px;
    }
    .portal-header h1 {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    /* 3. Dropdown Cards Container */
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    /* 4. Expander Header Styling */
    .streamlit-expanderHeader {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #1e3c72 !important;
        background-color: #f0f4f8 !important;
        border-radius: 8px !important;
    }

    /* 5. Custom Button Styles */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(21, 101, 192, 0.3) !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #1565C0 0%, #0D47A1 100%) !important;
        box-shadow: 0 4px 10px rgba(13, 71, 161, 0.4) !important;
    }

    div[data-testid="stButton"] > button[kind="secondary"] {
        background: linear-gradient(90deg, #2E7D32 0%, #1B5E20 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 5px rgba(27, 94, 32, 0.3) !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: linear-gradient(90deg, #1B5E20 0%, #0A3B0E 100%) !important;
        color: white !important;
        box-shadow: 0 4px 10px rgba(10, 59, 14, 0.4) !important;
    }

    /* 6. Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0;
    }

    .section-title-pmjjby {
        color: #1565C0;
        border-bottom: 2px solid #1565C0;
        padding-bottom: 5px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .section-title-pmsby {
        color: #2E7D32;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 5px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Google Sheet link
sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        if 'MANDAL' in df.columns:
            df['MANDAL'] = df['MANDAL'].astype(str).str.strip().str.title()
        return df
    except Exception as e:
        st.error(f'డేటా లోడ్ చేయడంలో విఫలమైంది: {e}')
        return None


df = load_data()

if df is not None:
    col_pmjjby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMJJBY'
    )
    col_pmjjby_bank = (
        'బ్యాంకు వారు ఎన్‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY'
    )
    col_pmsby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMSBY'
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

    # Update Data with Session Saved Entries
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

    # Sidebar Header and Downloads
    st.sidebar.header('📁 నావిగేషన్')
    st.sidebar.markdown('---')
    st.sidebar.markdown('### 📥 రిపోర్ట్‌లు డౌన్‌లోడ్')

    # 1. Entry chesina vivaralu (Entered Report)
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
        label='📥 1. నమోదు చేసిన వివరాలు (Entered)',
        data=entered_csv_report,
        file_name='Enrolled_Members_Report.csv',
        mime='text/csv',
        use_container_width=True,
    )

    # 2. Scheme-wise Done & Pending Reports
    temp_df = export_df_base.copy()
    temp_df['NUM_AGE'] = pd.to_numeric(temp_df['AGE'], errors='coerce').fillna(0)

    # PMJJBY Done
    pmjjby_done_df = temp_df[
        temp_df[col_pmjjby_sub].notna() | temp_df[col_pmjjby_bank].notna()
    ]
    pmjjby_done_csv = pmjjby_done_df.to_csv(index=False).encode('utf-8-sig')

    # PMJJBY Pending (Age 18 to 50 & Not Done)
    pmjjby_pending_df = temp_df[
        (temp_df['NUM_AGE'] >= 18)
        & (temp_df['NUM_AGE'] <= 50)
        & (temp_df[col_pmjjby_sub].isna())
        & (temp_df[col_pmjjby_bank].isna())
    ]
    pmjjby_pending_csv = pmjjby_pending_df.to_csv(index=False).encode('utf-8-sig')

    # PMSBY Done
    pmsby_done_df = temp_df[
        temp_df[col_pmsby_sub].notna() | temp_df[col_pmsby_bank].notna()
    ]
    pmsby_done_csv = pmsby_done_df.to_csv(index=False).encode('utf-8-sig')

    # PMSBY Pending (Age 18 to 70 & Not Done)
    pmsby_pending_df = temp_df[
        (temp_df['NUM_AGE'] >= 18)
        & (temp_df['NUM_AGE'] <= 70)
        & (temp_df[col_pmsby_sub].isna())
        & (temp_df[col_pmsby_bank].isna())
    ]
    pmsby_pending_csv = pmsby_pending_df.to_csv(index=False).encode('utf-8-sig')

    with st.sidebar.expander('🛡️ PMJJBY రిపోర్ట్‌లు'):
        st.download_button(
            label='✅ PMJJBY చేసినవి (Done)',
            data=pmjjby_done_csv,
            file_name='PMJJBY_Done_Report.csv',
            mime='text/csv',
            use_container_width=True,
        )
        st.download_button(
            label='⏳ PMJJBY చేయవలసినవి (Pending)',
            data=pmjjby_pending_csv,
            file_name='PMJJBY_Pending_Report.csv',
            mime='text/csv',
            use_container_width=True,
        )

    with st.sidebar.expander('🚑 PMSBY రిపోర్ట్‌లు'):
        st.download_button(
            label='✅ PMSBY చేసినవి (Done)',
            data=pmsby_done_csv,
            file_name='PMSBY_Done_Report.csv',
            mime='text/csv',
            use_container_width=True,
        )
        st.download_button(
            label='⏳ PMSBY చేయవలసినవి (Pending)',
            data=pmsby_pending_csv,
            file_name='PMSBY_Pending_Report.csv',
            mime='text/csv',
            use_container_width=True,
        )

    st.sidebar.markdown('---')

    # Page Navigation Radio Options
    app_mode = st.sidebar.radio(
        'పేజీ ఎంచుకోండి:',
        [
            '🏠 ఎన్‌రోల్మెంట్ డాష్‌బోర్డ్ (Portal)',
            '🏠 మండల్ వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal Wise Report)',
            '📊 VO వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal & VO Wise Report)',
            '👥 SHG & మెంబర్ వైజ్ రిపోర్ట్ (SHG / Member Level Detail)',
        ],
    )

    # PAGE 1: Enrollment Portal
    if app_mode == '🏠 ఎన్‌రోల్మెంట్ డాష్‌బోర్డ్ (Portal)':
        st.markdown(
            '<div class="portal-header"><h1>🔑 VOA & SHG Insurance Enrollment Portal</h1></div>',
            unsafe_allow_html=True,
        )

        mandals = ['-- ఎంచుకోండి --'] + sorted(
            export_df_base['MANDAL'].dropna().unique().tolist()
        )
        selected_mandal = st.selectbox('1. మండలం ఎంచుకోండి (Select Mandal):', mandals)

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
                selected_shg = st.selectbox('3. SHG group ఎంచుకోండి:', filtered_shgs)

        st.sidebar.markdown('---')

        if not selected_shg or selected_shg == '-- ఎంచుకోండి --':
            st.info(
                '👉 దయచేసి పైన ఇవ్వబడిన **మండలం, VO మరియు SHG గ్రూప్‌ను** వరుసగా ఎంచుకోండి.'
            )
            st.warning(
                '⚠️ SHG గ్రూప్‌ను ఎంచుకున్న తర్వాత 2వ పేజీలో SHG సభ్యుల పేర్లు మరియు వివరాలు కనిపించును.'
            )
        else:
            st.sidebar.success(
                f'📍 **ఎంచుకున్న వివరాలు:**\n\n- **మండలం:** {selected_mandal}\n- **VO:** {selected_vo}\n- **SHG:** {selected_shg}'
            )

            st.markdown(f'### 📄 పేజీ 2: SHG సభ్యుల జాబితా ({selected_shg})')
            st.success('నమోదు ప్రారంభించడానికి క్రింది సభ్యుల వివరాలను పూరించండి.')

            members_df = export_df_base[
                (export_df_base['MANDAL'] == selected_mandal)
                & (export_df_base['VO'] == selected_vo)
                & (export_df_base['SHG'] == selected_shg)
            ]

            for idx, row in members_df.reset_index(drop=True).iterrows():
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

                status_badge = (
                    ' | '.join(status_texts) if status_texts else 'ఎంట్రీ పెండింగ్'
                )

                with st.expander(
                    f'👤 {m_name} (ID: {m_id}) | వయస్సు: {raw_age} | Status: {status_badge}'
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

                            # 1. PMJJBY SECTION (18-50)
                            if 18 <= active_age <= 50:
                                st.markdown(
                                    '<h4 class="section-title-pmjjby">🛡️ 1. PMJJBY స్కీమ్ వివరాలు (18 నుండి 50 లోపు)</h4>',
                                    unsafe_allow_html=True,
                                )
                                bc1, bc2, bc3 = st.columns(3)
                                with bc1:
                                    st.text_input(
                                        'బ్యాంక్ పేరు (PMJJBY Bank)',
                                        value=str(
                                            row.get('BANK NAME', 'Indian Overseas Bank')
                                        ),
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
                                        value=str(
                                            row.get('MEMBER SB ACCOUNT NUMBER', '')
                                        ),
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
                                st.warning(
                                    'ℹ️ మెంబర్ వయస్సు 50 సంవత్సరాలు దాటడం వలన PMJJBY వర్తించదు.'
                                )
                                st.markdown('---')

                            # 2. PMSBY SECTION (18-70)
                            if 18 <= active_age <= 70:
                                st.markdown(
                                    '<h4 class="section-title-pmsby">🚑 2. PMSBY స్కీమ్ వివరాలు (18 నుండి 70 లోపు)</h4>',
                                    unsafe_allow_html=True,
                                )
                                pc1, pc2, pc3 = st.columns(3)
                                with pc1:
                                    st.text_input(
                                        'బ్యాంక్ పేరు (PMSBY Bank)',
                                        value=str(
                                            row.get('BANK NAME', 'Indian Overseas Bank')
                                        ),
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
                                        value=str(
                                            row.get('MEMBER SB ACCOUNT NUMBER', '')
                                        ),
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

                            # SAVE BUTTON
                            save_btn = st.button(
                                f'💾 {m_name} - అన్ని వివరాలు సేవ్ చేయండి (Save All)',
                                key=f'save_all_{idx}',
                                type='secondary',
                            )

                            if save_btn:
                                has_entered_any_date = (
                                    (pmjjby_sub_date is not None)
                                    or (pmjjby_b_date is not None)
                                    or (pmsby_sub_date is not None)
                                    or (pmsby_b_date_pmsby is not None)
                                )

                                if not has_entered_any_date:
                                    st.error(
                                        '❌ దయచేసి వివరాలు సేవ్ చేయడానికి PMJJBY లేదా PMSBY లో కనీసం ఒక తేదీని నమోదు చేయండి!'
                                    )
                                else:
                                    updated_row = row.to_dict()
                                    updated_row['AGE'] = str(active_age)
                                    updated_row['age correction'] = str(active_age)

                                    if active_age <= 50:
                                        if pmjjby_enrolled == 'Already Enrolled':
                                            if pmjjby_b_date is not None:
                                                updated_row[col_pmjjby_bank] = str(
                                                    pmjjby_b_date
                                                )
                                        else:
                                            if pmjjby_sub_date is not None:
                                                updated_row[col_pmjjby_sub] = str(
                                                    pmjjby_sub_date
                                                )
                                            if pmjjby_b_date is not None:
                                                updated_row[col_pmjjby_bank] = str(
                                                    pmjjby_b_date
                                                )

                                    if active_age <= 70:
                                        if pmsby_enrolled == 'Already Enrolled':
                                            if pmsby_b_date_pmsby is not None:
                                                updated_row[col_pmsby_bank] = str(
                                                    pmsby_b_date_pmsby
                                                )
                                        else:
                                            if pmsby_sub_date is not None:
                                                updated_row[col_pmsby_sub] = str(
                                                    pmsby_sub_date
                                                )
                                            if pmsby_b_date_pmsby is not None:
                                                updated_row[col_pmsby_bank] = str(
                                                    pmsby_b_date_pmsby
                                                )

                                    st.session_state.saved_entries_dict[m_id] = (
                                        updated_row
                                    )
                                    st.success(
                                        f'✅ {m_name} యొక్క అన్ని వివరాలు విజయవంతంగా సేవ్ చేయబడ్డాయి!'
                                    )
                                    st.toast(
                                        f'✅ {m_name} - All Details Saved Successfully!',
                                        icon='🎉',
                                    )
                                    st.rerun()
                    else:
                        st.warning(
                            '⚠️ దయచేసి వివరాలు నమోదు చేయడానికి ముందు "వయస్సును నిర్ధారించండి" బటన్ నొక్కండి.'
                        )

    # PAGE 2: Mandal Wise Abstract Report
    elif app_mode == '🏠 మండల్ వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal Wise Report)':
        st.markdown(
            '## 🏠 మండలాల వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్ (Mandal Wise Summary)'
        )
        st.write('---')

        mandal_summary = []
        for m_name, group in export_df_base.groupby('MANDAL'):
            total_members = len(group)
            pmjjby_sub = group[col_pmjjby_sub].notna().sum()
            pmjjby_enr = group[col_pmjjby_bank].notna().sum()
            pmsby_sub = group[col_pmsby_sub].notna().sum()
            pmsby_enr = group[col_pmsby_bank].notna().sum()
            total_enrolled = group[
                group[col_pmjjby_sub].notna()
                | group[col_pmjjby_bank].notna()
                | group[col_pmsby_sub].notna()
                | group[col_pmsby_bank].notna()
            ].shape[0]

            mandal_summary.append({
                'Mandal': m_name,
                'Total Members': total_members,
                'PMJJBY Submitted': pmjjby_sub,
                'PMJJBY Enrolled': pmjjby_enr,
                'PMSBY Submitted': pmsby_sub,
                'PMSBY Enrolled': pmsby_enr,
                'Total Total Updated': total_enrolled,
            })

        summary_df = pd.DataFrame(mandal_summary)
        st.dataframe(summary_df, use_container_width=True)

        csv_data = summary_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            '📥 డౌన్‌లోడ్ మండల్ రిపోర్ట్ (CSV)',
            data=csv_data,
            file_name='Mandal_Wise_Report.csv',
            mime='text/csv',
        )

    # PAGE 3: Mandal & VO Wise Report
    elif app_mode == '📊 VO వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal & VO Wise Report)':
        st.markdown('## 📊 VO వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్ (VO Wise Summary)')
        st.write('---')

        m_list = sorted(export_df_base['MANDAL'].dropna().unique().tolist())
        sel_m = st.selectbox('మండలం ఎంచుకోండి:', ['-- All Mandals --'] + m_list)

        filtered_data = export_df_base.copy()
        if sel_m != '-- All Mandals --':
            filtered_data = filtered_data[filtered_data['MANDAL'] == sel_m]

        vo_summary = []
        for (m_name, v_name), group in filtered_data.groupby(['MANDAL', 'VO']):
            total_members = len(group)
            pmjjby_sub = group[col_pmjjby_sub].notna().sum()
            pmjjby_enr = group[col_pmjjby_bank].notna().sum()
            pmsby_sub = group[col_pmsby_sub].notna().sum()
            pmsby_enr = group[col_pmsby_bank].notna().sum()
            total_updated = group[
                group[col_pmjjby_sub].notna()
                | group[col_pmjjby_bank].notna()
                | group[col_pmsby_sub].notna()
                | group[col_pmsby_bank].notna()
            ].shape[0]

            vo_summary.append({
                'Mandal': m_name,
                'VO Name': v_name,
                'Total Members': total_members,
                'PMJJBY Submitted': pmjjby_sub,
                'PMJJBY Enrolled': pmjjby_enr,
                'PMSBY Submitted': pmsby_sub,
                'PMSBY Enrolled': pmsby_enr,
                'Total Updated': total_updated,
            })

        vo_summary_df = pd.DataFrame(vo_summary)
        st.dataframe(vo_summary_df, use_container_width=True)

        vo_csv = vo_summary_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            '📥 డౌన్‌లోడ్ VO రిపోర్ట్ (CSV)',
            data=vo_csv,
            file_name='VO_Wise_Report.csv',
            mime='text/csv',
        )

    # PAGE 4: SHG & Member Level Detail
    elif app_mode == '👥 SHG & మెంబర్ వైజ్ రిపోర్ట్ (SHG / Member Level Detail)':
        st.markdown(
            '## 👥 SHG & మెంబర్ స్థాయి వివరాలు (SHG / Member Level Detail)'
        )
        st.write('---')

        c1, c2, c3 = st.columns(3)
        with c1:
            m_opt = st.selectbox(
                'మండలం:',
                ['-- All Mandals --']
                + sorted(export_df_base['MANDAL'].dropna().unique().tolist()),
            )

        vo_opts = ['-- All VOs --']
        if m_opt != '-- All Mandals --':
            vo_opts += sorted(
                export_df_base[export_df_base['MANDAL'] == m_opt]['VO']
                .dropna()
                .unique()
                .tolist()
            )
        with c2:
            v_opt = st.selectbox('VO:', vo_opts)

        shg_opts = ['-- All SHGs --']
        if v_opt != '-- All VOs --':
            shg_opts += sorted(
                export_df_base[
                    (export_df_base['MANDAL'] == m_opt)
                    & (export_df_base['VO'] == v_opt)
                ]['SHG']
                .dropna()
                .unique()
                .tolist()
            )
        with c3:
            s_opt = st.selectbox('SHG Group:', shg_opts)

        detail_df = export_df_base.copy()
        if m_opt != '-- All Mandals --':
            detail_df = detail_df[detail_df['MANDAL'] == m_opt]
        if v_opt != '-- All VOs --':
            detail_df = detail_df[detail_df['VO'] == v_opt]
        if s_opt != '-- All SHGs --':
            detail_df = detail_df[detail_df['SHG'] == s_opt]

        st.write(f'మొత్తం మెంబర్లు: **{len(detail_df)}**')
        st.dataframe(detail_df, use_container_width=True)

        member_csv = detail_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            '📥 వివరాల డేటా డౌన్‌లోడ్ చేసుకోండి (CSV)',
            data=member_csv,
            file_name='Member_Level_Detail_Report.csv',
            mime='text/csv',
        )
