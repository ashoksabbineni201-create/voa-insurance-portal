from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='VOA Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

# Custom CSS for styling categories in sidebar
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .portal-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 12px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
    }
    .portal-header h1 { color: #ffffff !important; font-size: 26px !important; }
    
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

sheet_id = '1vZqfSZmc24tEPCC-7D5B7oIGAujln7du'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'


@st.cache_data(ttl=60)
def load_data():
    try:
        df = pd.read_csv(sheet_url, dtype=str)
        df.columns = df.columns.str.strip()
        for col in ['MANDAL', 'VO', 'SHG', 'BANK NAME', 'BRANCH NAME']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip().str.upper()
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

    export_df_base['NUM_AGE'] = pd.to_numeric(
        export_df_base['AGE'], errors='coerce'
    ).fillna(0)

    # Sidebar Navigation Setup using st.sidebar.radio to prevent state sticking issues
    st.sidebar.markdown('📁 **NAVIGATOR / నావిగేషన్ మెను**')
    st.sidebar.markdown('---')

    nav_options = [
        '🏠 1. Enrollment Dashboard (Portal)',
        '📍 2. Mandal Wise Abstract Report',
        '📊 2. Mandal & VO Wise Abstract Report',
        '📥 2. Detailed Lists & Pending Reports',
        '👥 2. SHG Member Level Detailed Report',
        '🏛️ 3. Bank Wise Report',
        '📊 3. Bank Branch Wise Abstract Report',
    ]

    app_mode = st.sidebar.radio('మెను ఎంచుకోండి:', nav_options)
    st.sidebar.markdown('---')

    # PAGE 1: Enrollment Dashboard (Portal)
    if app_mode == nav_options[0]:
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
                '👉 దయచేసి పైన ఇవ్వబడిన **మండలం, VO మరియు SHG గ్రూప్‌‌ను** వరుసగా ఎంచుకోండి.'
            )
        else:
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

                        if 18 <= active_age <= 50:
                            st.markdown(
                                '<h4 class="section-title-pmjjby">🛡 1. PMJJBY స్కీమ్ వివరాలు (18-50)</h4>',
                                unsafe_allow_html=True,
                            )
                            bc1, bc2, bc3 = st.columns(3)
                            with bc1:
                                st.text_input('PMJJBY Bank', value=str(row.get('BANK NAME', '')), key=f'pmjjby_bank_{idx}')
                            with bc2:
                                st.text_input('PMJJBY Branch', value=str(row.get('BRANCH NAME', '')), key=f'pmjjby_branch_{idx}')
                            with bc3:
                                st.text_input('PMJJBY Acc No', value=str(row.get('MEMBER SB ACCOUNT NUMBER', '')), key=f'pmjjby_acc_{idx}')

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
                            st.rerun()

    # Mandal Wise Abstract Report
    elif app_mode == nav_options[1]:
        st.markdown('## 📍 Mandal Wise Abstract Report')
        st.write('---')
        scheme_choice = st.radio('స్కీమ్‌‌ను ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='m_scheme')

        mandal_summary = []
        for m_name, group in export_df_base.groupby('MANDAL'):
            if scheme_choice == '🛡️️ PMJJBY':
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmjjby_sub].notna() & elig[col_pmjjby_bank].isna()].shape[0]
            else:
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmsby_sub].notna() & elig[col_pmsby_bank].isna()].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)

            mandal_summary.append({
                'Mandal Name': m_name, 'Target': target, 'Enrolled': enrolled,
                'Balance': balance, 'Applications Submitted': submitted, 'Yet to Submit': yet_to_submit
            })
        st.dataframe(pd.DataFrame(mandal_summary), use_container_width=True)

    # Mandal & VO Wise Abstract Report
    elif app_mode == nav_options[2]:
        st.markdown('## 📊 Mandal & VO Wise Abstract Report')
        st.write('---')
        
        mandals_list = ['అన్నీ (All Mandals)'] + sorted(export_df_base['MANDAL'].dropna().unique().tolist())
        selected_mandal_filter = st.selectbox('మండలం ఎంచుకోండి (Select Mandal):', mandals_list)
        
        scheme_choice = st.radio('స్కీమ్‌ను ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='vo_scheme')
        
        filtered_df = export_df_base.copy()
        if selected_mandal_filter != 'అన్నీ (All Mandals)':
            filtered_df = filtered_df[filtered_df['MANDAL'] == selected_mandal_filter]

        vo_summary = []
        for (mandal, vo), group in filtered_df.groupby(['MANDAL', 'VO']):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmjjby_sub].notna() & elig[col_pmjjby_bank].isna()].shape[0]
            else:
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmsby_sub].notna() & elig[col_pmsby_bank].isna()].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)
            vo_summary.append({'Mandal Name': mandal, 'VO Name': vo, 'Target': target, 'Enrolled': enrolled, 'Balance': balance, 'Applications Submitted': submitted, 'Yet to Submit': yet_to_submit})

        st.dataframe(pd.DataFrame(vo_summary), use_container_width=True)

    # Detailed Lists & Pending Reports
    elif app_mode == nav_options[3]:
        st.markdown('## 📥 Detailed Lists & Pending Reports')
        st.write('---')

        report_type = st.selectbox(
            'రిపోర్ట్ రకం ఎంచుకోండి:',
            [
                '1. ఇప్పటివరకు ఎన్రోల్ అయినవారు (Completed / Enrolled List)',
                '2. అప్లికేషన్ బ్యాంకుకు ఇచ్చి, ఎన్రోల్ కానివారు (Submitted & Pending at Bank)',
                '3. ఇంకా బ్యాంకుకు అప్లికేషన్ ఇవ్వనివారు (Yet to Submit to Bank)'
            ]
        )

        scheme_filter = st.radio('స్కీమ్ ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True)
        is_pmjjby = (scheme_filter == '🛡️ PMJJBY')

        area_scope = st.radio('స్థాయి ఎంచుకోండి:', ['🌐 జిల్లా అంతా (Entire District)', '📍 నిర్దిష్ట మండలం (Specific Mandal)'], horizontal=True)

        target_df = export_df_base.copy()
        if area_scope == '📍 నిర్దిష్ట మండలం (Specific Mandal)':
            mandals_list_det = sorted(target_df['MANDAL'].dropna().unique().tolist())
            chosen_mandal = st.selectbox('మండలం ఎంచుకోండి:', mandals_list_det)
            target_df = target_df[target_df['MANDAL'] == chosen_mandal]

        result_list = []
        if '1.' in report_type:
            if is_pmjjby:
                result_list = target_df[(target_df['NUM_AGE'] >= 18) & (target_df['NUM_AGE'] <= 50) & (target_df[col_pmjjby_bank].notna())]
            else:
                result_list = target_df[(target_df['NUM_AGE'] >= 18) & (target_df['NUM_AGE'] <= 70) & (target_df[col_pmsby_bank].notna())]
        elif '2.' in report_type:
            if is_pmjjby:
                result_list = target_df[(target_df['NUM_AGE'] >= 18) & (target_df['NUM_AGE'] <= 50) & (target_df[col_pmjjby_sub].notna()) & (target_df[col_pmjjby_bank].isna())]
            else:
                result_list = target_df[(target_df['NUM_AGE'] >= 18) & (target_df['NUM_AGE'] <= 70) & (target_df[col_pmsby_sub].notna()) & (target_df[col_pmsby_bank].isna())]
        else:
            if is_pmjjby:
                result_list = target_df[(target_df['NUM_AGE'] >= 18) & (target_df['NUM_AGE'] <= 50) & (target_df[col_pmjjby_sub].isna()) & (target_df[col_pmjjby_bank].isna())]
            else:
                result_list = target_df[(target_df['NUM_AGE'] >= 18) & (target_df['NUM_AGE'] <= 70) & (target_df[col_pmsby_sub].isna()) & (target_df[col_pmsby_bank].isna())]

        st.markdown(f'### 📋 సభ్యుల జాబితా (మొత్తం రికార్డులు: {len(result_list)})')

        if not result_list.empty:
            display_cols = ['MANDAL', 'VO', 'SHG', 'MEMBER NAME', 'MEMBER ID', 'AGE', 'BANK NAME', 'BRANCH NAME', 'MEMBER SB ACCOUNT NUMBER']
            if is_pmjjby:
                display_cols += [col_pmjjby_sub, col_pmjjby_bank]
            else:
                display_cols += [col_pmsby_sub, col_pmsby_bank]

            final_display_df = result_list[[c for c in display_cols if c in result_list.columns]]
            st.dataframe(final_display_df, use_container_width=True)

            csv_data = final_display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='📥 ఈ రిపోర్ట్‌ని CSV గా డౌన్లోడ్ చేసుకోండి',
                data=csv_data,
                file_name=f'Insurance_Report_{report_type[:3]}_{scheme_filter[2:]}.csv',
                mime='text/csv',
                type='primary'
            )
        else:
            st.info('👉 ఈ ఫిల్టర్‌కు సరిపోయే రికార్డులు ఏవీ కనుగొనబడలేదు.')

    # SHG Member Level Detailed Report
    elif app_mode == nav_options[4]:
        st.markdown('## 👥 SHG Member Level Detailed Report')
        st.write('---')
        selected_mandal_filter = st.selectbox('మండలం ద్వారా ఫిల్టర్ చేయండి:', ['అన్నీ (All)'] + sorted(export_df_base['MANDAL'].dropna().unique().tolist()))
        
        filtered_report_df = export_df_base.copy()
        if selected_mandal_filter != 'అన్నీ (All)':
            filtered_report_df = filtered_report_df[filtered_report_df['MANDAL'] == selected_mandal_filter]

        st.dataframe(filtered_report_df[['MANDAL', 'VO', 'SHG', 'MEMBER NAME', 'MEMBER ID', 'AGE', col_pmjjby_sub, col_pmjjby_bank, col_pmsby_sub, col_pmsby_bank]], use_container_width=True)

    # Bank Wise Report
    elif app_mode == nav_options[5]:
        st.markdown('## 🏛️ Bank Wise Report')
        st.write('---')
        scheme_choice = st.radio('స్కీమ్‌ను ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='bank_wise_scheme')

        bank_summary = []
        for bank, group in export_df_base.groupby('BANK NAME'):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmjjby_sub].notna() & elig[col_pmjjby_bank].isna()].shape[0]
            else:
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmsby_sub].notna() & elig[col_pmsby_bank].isna()].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)
            bank_summary.append({'Bank Name': bank, 'Target': target, 'Enrolled': enrolled, 'Balance': balance, 'Applications Submitted': submitted, 'Yet to Submit': yet_to_submit})

        st.dataframe(pd.DataFrame(bank_summary), use_container_width=True)

    # Bank Branch Wise Abstract Report
    elif app_mode == nav_options[6]:
        st.markdown('## 📊 Bank Branch Wise Abstract Report')
        st.write('---')
        
        banks_list = ['అన్నీ (All Banks)'] + sorted(export_df_base['BANK NAME'].dropna().unique().tolist())
        selected_bank_filter = st.selectbox('బ్యాంక్ ఎంచుకోండి (Select Bank):', banks_list)
        
        scheme_choice = st.radio('స్కీమ్‌ను ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='b_scheme')

        filtered_bank_df = export_df_base.copy()
        if selected_bank_filter != 'అన్నీ (All Banks)':
            filtered_bank_df = filtered_bank_df[filtered_bank_df['BANK NAME'] == selected_bank_filter]

        bank_branch_summary = []
        for (bank, branch), group in filtered_bank_df.groupby(['BANK NAME', 'BRANCH NAME']):
            if scheme_choice == '🛡️ PMJJBY':
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 50)]
                target = len(elig)
                enrolled = elig[elig[col_pmjjby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmjjby_sub].notna() & elig[col_pmjjby_bank].isna()].shape[0]
            else:
                elig = group[(group['NUM_AGE'] >= 18) & (group['NUM_AGE'] <= 70)]
                target = len(elig)
                enrolled = elig[elig[col_pmsby_bank].notna()].shape[0]
                submitted = elig[elig[col_pmsby_sub].notna() & elig[col_pmsby_bank].isna()].shape[0]

            balance = max(0, target - enrolled)
            yet_to_submit = max(0, balance - submitted)
            bank_branch_summary.append({'Bank Name': bank, 'Branch Name': branch, 'Target': target, 'Enrolled': enrolled, 'Balance': balance, 'Applications Submitted': submitted, 'Yet to Submit': yet_to_submit})

        st.dataframe(pd.DataFrame(bank_branch_summary), use_container_width=True)
