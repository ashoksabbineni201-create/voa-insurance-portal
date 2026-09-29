from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS - App styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
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
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    .streamlit-expanderHeader {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #1e3c72 !important;
        background-color: #f0f4f8 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 8px 16px !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: linear-gradient(90deg, #2E7D32 0%, #1B5E20 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 8px 16px !important;
    }
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
        if 'BANK NAME' in df.columns:
            df['BANK NAME'] = df['BANK NAME'].astype(str).str.strip().str.upper()
        if 'BRANCH NAME' in df.columns:
            df['BRANCH NAME'] = df['BRANCH NAME'].astype(str).str.strip().str.upper()
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

    export_df_base['NUM_AGE'] = pd.to_numeric(export_df_base['AGE'], errors='coerce').fillna(0)
    
    export_df_base['PMJJBY_STATUS'] = 'Pending'
    export_df_base.loc[
        export_df_base[col_pmjjby_sub].notna() | export_df_base[col_pmjjby_bank].notna(),
        'PMJJBY_STATUS'
    ] = 'Done'

    export_df_base['PMSBY_STATUS'] = 'Pending'
    export_df_base.loc[
        export_df_base[col_pmsby_sub].notna() | export_df_base[col_pmsby_bank].notna(),
        'PMSBY_STATUS'
    ] = 'Done'

    # Sidebar Navigation
    st.sidebar.header('📁 నావిగేషన్')
    st.sidebar.markdown('---')

    app_mode = st.sidebar.radio(
        'పేజీ ఎంచుకోండి:',
        [
            '🏠 ఎన్‌రోల్మెంట్ డాష్‌బోర్డ్ (Portal)',
            '🏠 మండల్ వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal Wise Report)',
            '📊 బ్యాంక్ & బ్రాంచ్ వైజ్ అబ్‌స్ట్రాక్ట్ (Bank & Branch Wise Report)',
            '📊 VO వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal & VO Wise Report)',
            '👥 SHG & మెంబర్ వైజ్ రిపోర్ట్ (SHG / Member Level Detail)',
        ],
    )

    st.sidebar.markdown('---')

    # PAGE 1: Portal
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
                selected_shg = st.selectbox('3. SHG గ్రూప్ ఎంచుకోండి:', filtered_shgs)

        if not selected_shg or selected_shg == '-- ఎంచుకోండి --':
            st.info(
                '👉 దయచేసి పైన ఇవ్వబడిన **మండలం, VO మరియు SHG గ్రూప్‌ను** వరుసగా ఎంచుకోండి.'
            )
        else:
            st.sidebar.success(
                f'📍 **ఎంచుకున్న వివరాలు:**\n\n- **మండలం:** {selected_mandal}\n- **VO:** {selected_vo}\n- **SHG:** {selected_shg}'
            )

            st.markdown(f'### 📄 SHG సభ్యుల జాబితా ({selected_shg})')
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

                with st.expander(f'👤 {m_name} (ID: {m_id}) | వయస్సు: {raw_age}'):
                    entered_age = st.number_input(
                        'మెంబర్ వయస్సు నిర్ధారించండి / మార్చండి (Age):',
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

                        pmjjby_sub_date, pmjjby_b_date = None, None
                        pmsby_sub_date, pmsby_b_date_pmsby = None, None
                        pmjjby_enrolled, pmsby_enrolled = 'Not Enrolled', 'Not Enrolled'

                        if 18 <= active_age <= 50:
                            st.markdown(
                                '<h4 class="section-title-pmjjby">🛡️ 1. PMJJBY స్కీమ్ వివరాలు (18-50)</h4>',
                                unsafe_allow_html=True,
                            )
                            bc1, bc2, bc3 = st.columns(3)
                            with bc1:
                                st.text_input('PMJJBY Bank', value=str(row.get('BANK NAME', '')), key=f'pmjjby_bank_{idx}')
                            with bc2:
                                st.text_input('PMJJBY Branch', value=str(row.get('BRANCH NAME', '')), key=f'pmjjby_branch_{idx}')
                            with bc3:
                                st.text_input('PMJJBY Acc No', value=str(row.get('MEMBER SB ACCOUNT NUMBER', '')), key=f'pmjjby_acc_{idx}')

                            pmjjby_enrolled = st.radio('PMJJBY Status', ['Not Enrolled', 'Already Enrolled'], key=f'pmjjby_status_{idx}')
                            if pmjjby_enrolled == 'Already Enrolled':
                                pmjjby_b_date = st.date_input('Bank Enrolled Date - PMJJBY', value=None, key=f'pmjjby_b_already_{idx}')
                            else:
                                col_d1, col_d2 = st.columns(2)
                                with col_d1:
                                    pmjjby_sub_date = st.date_input('Application Submitted Date - PMJJBY', value=None, key=f'pmjjby_sub_{idx}')
                                with col_d2:
                                    pmjjby_b_date = st.date_input('Bank Enrolled Date - PMJJBY', value=None, key=f'pmjjby_b_opt_{idx}')

                        if 18 <= active_age <= 70:
                            st.markdown(
                                '<h4 class="section-title-pmsby">🚑 2. PMSBY స్కీమ్ వివరాలు (18-70)</h4>',
                                unsafe_allow_html=True,
                            )
                            pc1, pc2, pc3 = st.columns(3)
                            with pc1:
                                st.text_input('PMSBY Bank', value=str(row.get('BANK NAME', '')), key=f'pmsby_bank_{idx}')
                            with pc2:
                                st.text_input('PMSBY Branch', value=str(row.get('BRANCH NAME', '')), key=f'pmsby_branch_{idx}')
                            with pc3:
                                st.text_input('PMSBY Acc No', value=str(row.get('MEMBER SB ACCOUNT NUMBER', '')), key=f'pmsby_acc_{idx}')

                            pmsby_enrolled = st.radio('PMSBY Status', ['Not Enrolled', 'Already Enrolled'], key=f'pmsby_status_{idx}')
                            if pmsby_enrolled == 'Already Enrolled':
                                pmsby_b_date_pmsby = st.date_input('Bank Enrolled Date - PMSBY', value=None, key=f'pmsby_b_already_{idx}')
                            else:
                                col_d3, col_d4 = st.columns(2)
                                with col_d3:
                                    pmsby_sub_date = st.date_input('Application Submitted Date - PMSBY', value=None, key=f'pmsby_sub_{idx}')
                                with col_d4:
                                    pmsby_b_date_pmsby = st.date_input('Bank Enrolled Date - PMSBY', value=None, key=f'pmsby_b_opt_{idx}')

                        if st.button(f'💾 {m_name} వివరాలు సేవ్ చేయండి', key=f'save_{idx}', type='secondary'):
                            updated_row = row.to_dict()
                            updated_row['AGE'] = str(active_age)
                            if pmjjby_sub_date: updated_row[col_pmjjby_sub] = str(pmjjby_sub_date)
                            if pmjjby_b_date: updated_row[col_pmjjby_bank] = str(pmjjby_b_date)
                            if pmsby_sub_date: updated_row[col_pmsby_sub] = str(pmsby_sub_date)
                            if pmsby_b_date_pmsby: updated_row[col_pmsby_bank] = str(pmsby_b_date_pmsby)

                            st.session_state.saved_entries_dict[m_id] = updated_row
                            st.success(f'✅ {m_name} వివరాలు సేవ్ చేయబడ్డాయి!')
                            st.rer5un = getattr(st, 'rerun', None)
                            if st.rer5un: st.rer5un()

    # PAGE 2: Mandal Wise Report
    elif app_mode == '🏠 మండల్ వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal Wise Report)':
        st.markdown('## 🏠 మండలాల వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్ (Mandal Wise Summary)')
        st.write('---')

        scheme_choice = st.radio('స్కీమ్‌ను ఎంచుకోండి:', ['అన్ని స్కీమ్‌లు (All)', '🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True)

        mandal_summary = []
        for m_name, group in export_df_base.groupby('MANDAL'):
            total_members = len(group)
            pmjjby_eligible = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)].shape[0]
            pmsby_eligible = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)].shape[0]
            pmjjby_done = group[group['PMJJBY_STATUS'] == 'Done'].shape[0]
            pmsby_done = group[group['PMSBY_STATUS'] == 'Done'].shape[0]

            if scheme_choice == '🛡️ PMJJBY':
                mandal_summary.append({'Mandal': m_name, 'Total': total_members, 'Eligible': pmjjby_eligible, 'Done': pmjjby_done, 'Pending': max(0, pmjjby_eligible - pmjjby_done)})
            elif scheme_choice == '🚑 PMSBY':
                mandal_summary.append({'Mandal': m_name, 'Total': total_members, 'Eligible': pmsby_eligible, 'Done': pmsby_done, 'Pending': max(0, pmsby_eligible - pmsby_done)})
            else:
                mandal_summary.append({
                    'Mandal': m_name, 'Total Members': total_members,
                    'PMJJBY Eligible': pmjjby_eligible, 'PMJJBY Done': pmjjby_done, 'PMJJBY Pending': max(0, pmjjby_eligible - pmjjby_done),
                    'PMSBY Eligible': pmsby_eligible, 'PMSBY Done': pmsby_done, 'PMSBY Pending': max(0, pmsby_eligible - pmsby_done)
                })

        st.dataframe(pd.DataFrame(mandal_summary), use_container_width=True)

    # PAGE 3: Bank & Branch Wise Abstract Report
    elif app_mode == '📊 బ్యాంక్ & బ్రాంచ్ వైజ్ అబ్‌స్ట్రాక్ట్ (Bank & Branch Wise Report)':
        st.markdown('## 📊 బ్యాంక్ మరియు బ్రాంచ్ వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్')
        st.write('---')

        scheme_choice = st.radio('స్కీమ్‌ను ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='bank_scheme')

        if 'BANK NAME' in export_df_base.columns and 'BRANCH NAME' in export_df_base.columns:
            bank_summary = []
            for (bank, branch), group in export_df_base.groupby(['BANK NAME', 'BRANCH NAME']):
                total_members = len(group)
                if scheme_choice == '🛡️ PMJJBY':
                    eligible = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)].shape[0]
                    done = group[group['PMJJBY_STATUS'] == 'Done'].shape[0]
                else:
                    eligible = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)].shape[0]
                    done = group[group['PMSBY_STATUS'] == 'Done'].shape[0]
                
                bank_summary.append({
                    'Bank Name': bank,
                    'Branch Name': branch,
                    'Total Members': total_members,
                    'Eligible': eligible,
                    'Enrolled / Done': done,
                    'Pending': max(0, eligible - done)
                })

            st.dataframe(pd.DataFrame(bank_summary), use_container_width=True)
        else:
            st.error("డేటాలో బ్యాంక్ లేదా బ్రాంచ్ కాలమ్‌లు అందుబాటులో లేవు.")

    # PAGE 4: VO Wise Abstract
    elif app_mode == '📊 VO వైజ్ అబ్‌స్ట్రాక్ట్ & రిపోర్ట్ (Mandal & VO Wise Report)':
        st.markdown('## 📊 VO ల వారీగా అబ్‌స్ట్రాక్ట్ రిపోర్ట్')
        st.write('---')

        vo_summary = []
        for (mandal, vo), group in export_df_base.groupby(['MANDAL', 'VO']):
            vo_summary.append({
                'Mandal': mandal, 'VO Name': vo,
                'Total Members': len(group),
                'PMJJBY Done': group[group['PMJJBY_STATUS'] == 'Done'].shape[0],
                'PMSBY Done': group[group['PMSBY_STATUS'] == 'Done'].shape[0]
            })
        st.dataframe(pd.DataFrame(vo_summary), use_container_width=True)

    # PAGE 5: SHG & Member Level Detail
    elif app_mode == '👥 SHG & మెంబర్ వైజ్ రిపోర్ట్ (SHG / Member Level Detail)':
        st.markdown('## 👥 SHG మరియు సభ్యుల పూర్తి వివరాల నివేదిక')
        st.write('---')
        selected_mandal_filter = st.selectbox('మండలం ద్వారా ఫిల్టర్ చేయండి:', ['అన్నీ (All)'] + sorted(export_df_base['MANDAL'].dropna().unique().tolist()))
        
        filtered_report_df = export_df_base.copy()
        if selected_mandal_filter != 'అన్నీ (All)':
            filtered_report_df = filtered_report_df[filtered_report_df['MANDAL'] == selected_mandal_filter]

        st.dataframe(filtered_report_df[['MANDAL', 'VO', 'SHG', 'MEMBER NAME', 'MEMBER ID', 'AGE', 'PMJJBY_STATUS', 'PMSBY_STATUS']], use_container_width=True)
