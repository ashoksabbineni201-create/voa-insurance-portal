from datetime import date
import pandas as pd
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


def trigger_rerun():
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except Exception:
            pass


df = load_data()

if df is not None:
    col_pmjjby_sub = (
        'అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted at Bank) - PMJJBY'
    )
    col_pmjjby_bank = (
        'బ్యాంకు వారు ఎన్‌‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMJJBY'
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

    if 'name_corrections_log' not in st.session_state:
        st.session_state.name_corrections_log = {}

    if 'age_corrections_log' not in st.session_state:
        st.session_state.age_corrections_log = {}

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

    # Header Title
    st.markdown(
        '<div class="portal-header"><h1>గుంటూరు జిల్లా - SHG సభ్యుల బీమా (PMJJBY & PMSBY) ఎన్‌రోల్మెంట్ పోర్టల్</h1><p>సంఘ సభ్యులందరికీ సులభంగా ఇన్సూరెన్స్ నమోదు మరియు ట్రాకింగ్ చేయు విధానం</p></div>',
        unsafe_allow_html=True,
    )

    nav_options_mapping = {
        '1️⃣ 🏠 డాష్‌‌బోర్డ్ (Dashboard & Entry)': 'Dashboard',
        '2️⃣ 📍 మండలం వారీగా రిపోర్ట్ (Mandal Wise)': 'Mandal Wise',
        '3️⃣ 📊 వి.ఓ (VO) వారీగా రిపోర్ట్ (VO Wise)': 'VO Wise',
        '4️⃣ 🏛️ బ్యాంక్ వారీగా రిపోర్ట్ (Bank Wise)': 'Bank Wise',
        '5️⃣ 📈 బ్రాంచ్ వారీగా రిపోర్ట్ (Branch Wise)': 'Branch Wise',
        '6️⃣ 📥 పెండింగ్ జాబితా (Pending Reports)': 'Pending Reports',
        '7️⃣ 👥 పూర్తి సభ్యుల జాబితా (Member Level)': 'Member Level',
        '8️⃣ ✏️ నేమ్ కరెక్షన్ నివేదిక (Name Corrections)': 'Name Corrections',
        '9️⃣ 🔢 ఏజ్ కరెక్షన్ నివేదిక (Age Corrections)': 'Age Corrections'
    }

    selected_display_opt = st.selectbox(
        '📌 దయచేసి క్రింది మెను నుండి కావలసిన సెక్షన్ లేదా రిపోర్ట్ ఎంచుకోండి:',
        list(nav_options_mapping.keys()),
        key='mobile_friendly_main_nav'
    )
    
    app_mode = nav_options_mapping[selected_display_opt]
    st.markdown('---')

    # PAGE 1: DASHBOARD
    if app_mode == 'Dashboard':
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
                '👉 దయచేసి పైన ఇవ్వబడిన **మండలం, VO మరియు SHG గ్రూప్ను** వరుసగా ఎంచుకోండి.'
            )
        else:
            st.markdown(f'### 📄 SHG సభ్యుల జాబితా: <span style="color: #15803d;">{selected_shg}</span>', unsafe_allow_html=True)
            members_df = export_df_base[
                (export_df_base['MANDAL'] == selected_mandal)
                & (export_df_base['VO'] == selected_vo)
                & (export_df_base['SHG'] == selected_shg)
            ]

            for idx, row in members_df.reset_index(drop=True).iterrows():
                m_id = str(row.get('MEMBER ID', f'ID-{idx+1}'))
                current_row = st.session_state.saved_entries_dict.get(m_id, row)
                
                original_row_data = df[df['MEMBER ID'].astype(str) == str(m_id)]
                orig_name = str(original_row_data.iloc[0]['MEMBER NAME']).strip().upper() if not original_row_data.empty else str(row.get('MEMBER NAME', '')).strip().upper()
                orig_age = str(original_row_data.iloc[0]['AGE']).strip() if not original_row_data.empty else str(row.get('AGE', '35')).strip()

                m_name = str(current_row.get('MEMBER NAME', 'Unknown'))
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
                    status_tags.append("❌ Not Eligible")
                else:
                    if pd.notna(p_bank) and str(p_bank).lower() != 'nan' and str(p_bank).strip() != '':
                        status_tags.append("🛡️ PMJJBY Enrolled")
                    elif pd.notna(p_sub) and str(p_sub).lower() != 'nan' and str(p_sub).strip() != '':
                        status_tags.append("🛡️ PMJJBY Application Submitted")

                    if pd.notna(s_bank) and str(s_bank).lower() != 'nan' and str(s_bank).strip() != '':
                        status_tags.append("🚑 PMSBY Enrolled")
                    elif pd.notna(s_sub) and str(s_sub).lower() != 'nan' and str(s_sub).strip() != '':
                        status_tags.append("🚑 PMSBY Application Submitted")

                    if not status_tags:
                        status_tags.append("⏳ అప్డేషన్ పెండింగ్ (Pending)")

                status_str = " | ".join(status_tags)

                with st.expander(f'👤 {m_name} | వయస్సు: {raw_age} -- [{status_str}]'):
                    
                    col_nc1, col_nc2 = st.columns([2, 1])
                    with col_nc1:
                        entered_name = st.text_input(
                            'సభ్యురాలి పేరు (ఆధార్ ప్రకారం సరిచూసుకోండి):',
                            value=m_name,
                            key=f'name_{idx}'
                        )
                    with col_nc2:
                        entered_age = st.number_input(
                            'వయస్సు (Age):',
                            min_value=1,
                            max_value=100,
                            value=raw_age,
                            key=f'age_{idx}',
                        )

                    is_confirmed_key = f'is_age_confirmed_{idx}'
                    has_saved_before = m_id in st.session_state.saved_entries_dict
                    
                    if not st.session_state.get(is_confirmed_key, False) and not has_saved_before:
                        age_confirmed = st.button(
                            f'✔️ {m_name} పేరు మరియు వయస్సు నిర్ధారించండి',
                            key=f'confirm_age_btn_{idx}',
                            type='primary',
                        )
                        if age_confirmed:
                            st.session_state[is_confirmed_key] = True
                            trigger_rerun()
                    
                    if st.session_state.get(is_confirmed_key, False) or has_saved_before:
                        active_age = entered_age

                        if active_age > 70:
                            st.error("❌ ఈ సభ్యురాలు 70 సంవత్సరాలు దాటినందున బీమా పథకాలకు అర్హులు కాదు (Not Eligible).")
                        else:
                            pmjjby_sub_date, pmjjby_b_date = None, None
                            pmsby_sub_date, pmsby_b_date_pmsby = None, None

                            def safe_parse_date(val):
                                if pd.isna(val) or not val or str(val).lower() == 'nan':
                                    return None
                                try:
                                    return pd.to_datetime(val).date()
                                except:
                                    return None

                            existing_pm_sub = safe_parse_date(current_row.get(col_pmjjby_sub))
                            existing_pm_bank = safe_parse_date(current_row.get(col_pmjjby_bank))
                            existing_ps_sub = safe_parse_date(current_row.get(col_pmsby_sub))
                            existing_ps_bank = safe_parse_date(current_row.get(col_pmsby_bank))

                            if 18 <= active_age <= 50:
                                st.markdown(
                                    '<div class="section-title-pmjjby">🛡 1. PMJJBY స్కీమ్ వివరాలు (18-50 సంవత్సరాలు)</div>',
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
                                    pmjjby_sub_date = st.date_input('Application Submitted Date - PMJJBY (అప్లికేషన్ తేదీ ఇవ్వాలి)', value=existing_pm_sub, key=f'pmjjby_sub_{idx}')
                                with col_d2:
                                    pmjjby_b_date = st.date_input('Bank Enrolled Date - PMJJBY', value=existing_pm_bank, key=f'pmjjby_b_opt_{idx}')

                            if 18 <= active_age <= 70:
                                st.markdown(
                                    '<div class="section-title-pmsby">🚑 2. PMSBY స్కీమ్ వివరాలు (18-70 సంవత్సరాలు)</div>',
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
                                    pmsby_sub_date = st.date_input('Application Submitted Date - PMSBY (అప్లికేషన్ తేదీ ఇవ్వాలి)', value=existing_ps_sub, key=f'pmsby_sub_{idx}')
                                with col_d4:
                                    pmsby_b_date_pmsby = st.date_input('Bank Enrolled Date - PMSBY', value=existing_ps_bank, key=f'pmsby_b_opt_{idx}')

                            if st.button(f'💾 {entered_name} వివరాలు సేవ్ చేయండి', key=f'save_{idx}', type='primary'):
                                date_error = False
                                
                                if pmjjby_b_date and not pmjjby_sub_date:
                                    date_error = True
                                    st.error("❌ PMJJBY లో: ముందుగా అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted Date) ఇవ్వకుండా, నేరుగా బ్యాంకు ఎన్‌రోల్ చేసిన తేదీ ఇవ్వకూడదు!")
                                
                                if pmsby_b_date_pmsby and not pmsby_sub_date:
                                    date_error = True
                                    st.error("❌ PMSBY లో: ముందుగా అప్లికేషన్ బ్యాంకుకు సబ్మిట్ చేసిన తేదీ (Application Submitted Date) ఇవ్వకుండా, నేరుగా బ్యాంకు ఎన్‌‌రోల్ చేసిన తేదీ ఇవ్వకూడదు!")

                                if not date_error and pmjjby_sub_date and pmjjby_b_date:
                                    if pmjjby_b_date < pmjjby_sub_date:
                                        date_error = True
                                        st.error("❌ PMJJBY లో: బ్యాంకు ఎన్‌రోల్ చేసిన తేదీ, అప్లికేషన్ సబ్మిట్ చేసిన తేదీ కంటే ముందు ఉండకూడదు!")

                                if not date_error and pmsby_sub_date and pmsby_b_date_pmsby:
                                    if pmsby_b_date_pmsby < pmsby_sub_date:
                                        date_error = True
                                        st.error("❌ PMSBY లో: బ్యాంకు ఎన్‌రోల్ చేసిన తేదీ, అప్లికేషన్ సబ్మిట్ చేసిన తేదీ కంటే ముందు ఉండకూడదు!")

                                if not date_error:
                                    updated_row = row.to_dict()
                                    cleaned_new_name = str(entered_name).strip().upper()
                                    updated_row['MEMBER NAME'] = cleaned_new_name
                                    updated_row['AGE'] = str(active_age)
                                    
                                    # Log Name Correction (Member Name stores Old Name, Corrected Name stores New Name)
                                    if cleaned_new_name != orig_name:
                                        st.session_state.name_corrections_log[m_id] = {
                                            'Mandal Name': str(row.get('MANDAL', '')),
                                            'VO Name': str(row.get('VO', '')),
                                            'SHG Name': str(row.get('SHG', '')),
                                            'Member Name': orig_name,
                                            'Member ID': str(m_id),
                                            'Corrected Name': cleaned_new_name
                                        }
                                    elif m_id in st.session_state.name_corrections_log:
                                        del st.session_state.name_corrections_log[m_id]

                                    # Log Age Correction
                                    if str(active_age) != str(orig_age):
                                        st.session_state.age_corrections_log[m_id] = {
                                            'Mandal Name': str(row.get('MANDAL', '')),
                                            'VO Name': str(row.get('VO', '')),
                                            'SHG Name': str(row.get('SHG', '')),
                                            'Member Name': cleaned_new_name,
                                            'Member ID': str(m_id),
                                            'Old Age': orig_age,
                                            'New Age': str(active_age)
                                        }
                                    elif m_id in st.session_state.age_corrections_log:
                                        del st.session_state.age_corrections_log[m_id]
                                    
                                    if pmjjby_sub_date: 
                                        updated_row[col_pmjjby_sub] = str(pmjjby_sub_date)
                                    if pmjjby_b_date: 
                                        updated_row[col_pmjjby_bank] = str(pmjjby_b_date)
                                    if pmsby_sub_date: 
                                        updated_row[col_pmsby_sub] = str(pmsby_sub_date)
                                    if pmsby_b_date_pmsby: 
                                        updated_row[col_pmsby_bank] = str(pmsby_b_date_pmsby)

                                    st.session_state.saved_entries_dict[m_id] = updated_row
                                    st.success(f'✅ {cleaned_new_name} వివరాలు విజయవంతంగా సేవ్ చేయబడ్డాయి!')
                                    trigger_rerun()

    # 2. MANDAL WISE
    elif app_mode == 'Mandal Wise':
        st.markdown("## 📍 మండలం వారీగా సారాంశం (Mandal Wise)")
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

    # 3. VO WISE
    elif app_mode == 'VO Wise':
        st.markdown("## 📊 వి.ఓ (VO) వారీగా సారాంశం")
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

    # 4. BANK WISE
    elif app_mode == 'Bank Wise':
        st.markdown("## 🏛️ బ్యాంక్ వారీగా సారాంశం")
        st.write('---')
        scheme_choice = st.radio('స్కీమ్‌‌ను ఎంచుకోండి:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='bank_wise_scheme')

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

    # 5. BRANCH WISE
    elif app_mode == 'Branch Wise':
        st.markdown("## 📈 బ్రాంచ్ వారీగా సారాంశం")
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

    # 6. PENDING LIST
    elif app_mode == 'Pending Reports':
        st.markdown("## 📥 పెండింగ్ మరియు ఎన్‌రోల్‌మెంట్ నివేదికలు")
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
                mime='text/css',
                type='primary'
            )
        else:
            st.info('👉 ఈ ఫిల్టర్‌కు సరిపోయే రికార్డులు ఏవీ కనుగొనబడలేదు.')

    # 7. MEMBER LEVEL LIST
    elif app_mode == 'Member Level':
        st.markdown("## 👥 పూర్తి సభ్యుల జాబితా")
        st.write('---')
        selected_mandal_filter = st.selectbox('మండలం ద్వారా ఫిల్టర్ చేయండి:', ['అన్నీ (All)'] + sorted(export_df_base['MANDAL'].dropna().unique().tolist()))
        
        filtered_report_df = export_df_base.copy()
        if selected_mandal_filter != 'అన్నీ (All)':
            filtered_report_df = filtered_report_df[filtered_report_df['MANDAL'] == selected_mandal_filter]

        st.dataframe(filtered_report_df[['MANDAL', 'VO', 'SHG', 'MEMBER NAME', 'MEMBER ID', 'AGE', col_pmjjby_sub, col_pmjjby_bank, col_pmsby_sub, col_pmsby_bank]], use_container_width=True)

    # 8. NAME CORRECTIONS REPORT
    elif app_mode == 'Name Corrections':
        st.markdown("## ✏️ నేమ్ కరెక్షన్ చేసిన సభ్యుల నివేదిక (Name Corrections Report)")
        st.write('---')
        
        if len(st.session_state.name_corrections_log) > 0:
            name_corr_df = pd.DataFrame(list(st.session_state.name_corrections_log.values()))
            
            mandal_list_nc = ['అన్నీ (All)'] + sorted(name_corr_df['Mandal Name'].dropna().unique().tolist())
            chosen_m_nc = st.selectbox('మండలం వారీగా ఫిల్టర్ చేయండి:', mandal_list_nc, key='nc_mandal_filter')
            
            if chosen_m_nc != 'అన్నీ (All)':
                name_corr_df = name_corr_df[name_corr_df['Mandal Name'] == chosen_m_nc]
            
            st.markdown(f'### 📋 మొత్తం సవరించిన పేర్లు: {len(name_corr_df)}')
            st.dataframe(name_corr_df[['Mandal Name', 'VO Name', 'SHG Name', 'Member Name', 'Member ID', 'Corrected Name']], use_container_width=True)
            
            csv_nc = name_corr_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='📥 నేమ్ కరెక్షన్ రిపోర్ట్‌ని CSV గా డౌన్లోడ్ చేసుకోండి',
                data=csv_nc,
                file_name='Name_Corrections_Report.csv',
                mime='text/css',
                type='primary'
            )
        else:
            st.info('👉 ఇప్పటివరకు ఎలాంటి నేమ్ కరెక్షన్స్ నమోదు చేయబడలేదు.')

    # 9. AGE CORRECTIONS REPORT
    elif app_mode == 'Age Corrections':
        st.markdown("## 🔢 ఏజ్ కరెక్షన్ చేసిన సభ్యుల నివేదిక (Age Corrections Report)")
        st.write('---')
        
        if len(st.session_state.age_corrections_log) > 0:
            age_corr_df = pd.DataFrame(list(st.session_state.age_corrections_log.values()))
            
            mandal_list_ac = ['అన్నీ (All)'] + sorted(age_corr_df['Mandal Name'].dropna().unique().tolist())
            chosen_m_ac = st.selectbox('మండలం వారీగా ఫిల్టర్ చేయండి:', mandal_list_ac, key='ac_mandal_filter')
            
            if chosen_m_ac != 'అన్నీ (All)':
                age_corr_df = age_corr_df[age_corr_df['Mandal Name'] == chosen_m_ac]
            
            st.markdown(f'### 📋 మొత్తం సవరించిన వయస్సులు: {len(age_corr_df)}')
            st.dataframe(age_corr_df[['Mandal Name', 'VO Name', 'SHG Name', 'Member Name', 'Member ID', 'Old Age', 'New Age']], use_container_width=True)
            
            csv_ac = age_corr_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label='📥 ఏజ్ కరెక్షన్ రిపోర్ట్‌ని CSV గా డౌన్లోడ్ చేసుకోండి',
                data=csv_ac,
                file_name='Age_Corrections_Report.csv',
                mime='text/css',
                type='primary'
            )
        else:
            st.info('👉 ఇప్పటివరకు ఎలాంటి ఏజ్ కరెక్షన్స్ నమోదు చేయబడలేదు.')
