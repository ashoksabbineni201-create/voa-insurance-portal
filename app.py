from datetime import date
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title='Insurance Enrollment Portal', page_icon='🏛️', layout='wide'
)

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
        for col in ['MANDAL', 'VO', 'SHG', 'BANK NAME', 'BRANCH NAME', 'MEMBER SB ACCOUNT NUMBER']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        if 'BANK NAME' in df.columns:
            df['BANK NAME'] = df['BANK NAME'].str.upper()
        if 'BRANCH NAME' in df.columns:
            df['BRANCH NAME'] = df['BRANCH NAME'].str.upper()
        return df
    except Exception as e:
        st.error(f'Data load cheyadamlo vipalamaindi: {e}')
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
    all_available_banks = []
    if 'BANK NAME' in df.columns:
        all_available_banks = sorted(df['BANK NAME'].dropna().unique().tolist())
    if not all_available_banks:
        all_available_banks = ['SBI', 'UNION BANK', 'ANDHRA PRADESH GRAMEENA VIKAS BANK', 'APGVB', 'CANARA BANK']

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
        'బ్యాంకు వారు ఎన్‌‌రోల్ చేసిన తేదీ (Bank Enrolled Date) - PMSBY'
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

    if 'bank_corrections_log' not in st.session_state:
        st.session_state.bank_corrections_log = {}

    if 'acc_corrections_log' not in st.session_state:
        st.session_state.acc_corrections_log = {}

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

    st.markdown(
        '<div class="portal-header"><h1>Guntur District - SHG Members Insurance Portal</h1><p>Insurance Entry and Tracking System</p></div>',
        unsafe_allow_html=True,
    )

    nav_options_mapping = {
        '1️⃣ 🏠 Dashboard (Dashboard & Entry)': 'Dashboard',
        '2️⃣ 📍 Mandal Wise Report': 'Mandal Wise',
        '3️⃣ 📊 VO Wise Report': 'VO Wise',
        '4️⃣ 🏛️ Bank Wise Report': 'Bank Wise',
        '5️⃣ 📈 Branch Wise Report': 'Branch Wise',
        '6️⃣ 📥 Pending Reports': 'Pending Reports',
        '7️⃣ 👥 Member Level List': 'Member Level',
        '8️⃣ 📝 Corrections Report': 'Corrections Reports'
    }

    selected_display_opt = st.selectbox(
        '📌 Dayachesi kinda menu nundi kavalsina section lekha report ennukondi:',
        list(nav_options_mapping.keys()),
        key='mobile_friendly_main_nav'
    )
    
    app_mode = nav_options_mapping[selected_display_opt]
    st.markdown('---')

    if app_mode == 'Dashboard':
        mandals = ['-- Enchukondi --'] + sorted(
            export_df_base['MANDAL'].dropna().unique().tolist()
        )
        selected_mandal = st.selectbox('1. Mandal Enchukondi:', mandals)

        selected_vo = None
        selected_shg = None

        if selected_mandal and selected_mandal != '-- Enchukondi --':
            filtered_vos = ['-- Enchukondi --'] + sorted(
                export_df_base[export_df_base['MANDAL'] == selected_mandal]['VO']
                .dropna()
                .unique()
                .tolist()
            )
            selected_vo = st.selectbox(
                '2. VO (Village Organization) peru enchukondi:', filtered_vos
            )

            if selected_vo and selected_vo != '-- Enchukondi --':
                filtered_shgs = ['-- Enchukondi --'] + sorted(
                    export_df_base[
                        (export_df_base['MANDAL'] == selected_mandal)
                        & (export_df_base['VO'] == selected_vo)
                    ]['SHG']
                    .dropna()
                    .unique()
                    .tolist()
                )
                selected_shg = st.selectbox('3. SHG Group enchukondi:', filtered_shgs)

        if not selected_shg or selected_shg == '-- Enchukondi --':
            st.info(
                '👉 Dayachesi paina ivvabadina **Mandal, VO mariyu SHG Group** varusaga enchukondi.'
            )
        else:
            st.markdown(f'### 📄 SHG Members List: <span style="color: #15803d;">{selected_shg}</span>', unsafe_allow_html=True)
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
                orig_bank = str(original_row_data.iloc[0]['BANK NAME']).strip().upper() if not original_row_data.empty and 'BANK NAME' in original_row_data.columns else str(row.get('BANK NAME', '')).strip().upper()
                orig_branch = str(original_row_data.iloc[0]['BRANCH NAME']).strip().upper() if not original_row_data.empty and 'BRANCH NAME' in original_row_data.columns else str(row.get('BRANCH NAME', '')).strip().upper()
                orig_acc = str(original_row_data.iloc[0]['MEMBER SB ACCOUNT NUMBER']).strip() if not original_row_data.empty and 'MEMBER SB ACCOUNT NUMBER' in original_row_data.columns else str(row.get('MEMBER SB ACCOUNT NUMBER', '')).strip()

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
                        status_tags.append("⏳ Pending")

                status_str = " | ".join(status_tags)

                with st.expander(f'👤 {m_name} | Age: {raw_age} -- [{status_str}]'):
                    
                    col_nc1, col_nc2 = st.columns([2, 1])
                    with col_nc1:
                        entered_name = st.text_input(
                            'Member Name (Aadhar prakaram):',
                            value=m_name,
                            key=f'name_{idx}'
                        )
                    with col_nc2:
                        entered_age = st.number_input(
                            'Age:',
                            min_value=1,
                            max_value=100,
                            value=raw_age,
                            key=f'age_{idx}',
                        )

                    is_confirmed_key = f'is_age_confirmed_{idx}'
                    has_saved_before = m_id in st.session_state.saved_entries_dict
                    
                    if not st.session_state.get(is_confirmed_key, False) and not has_saved_before:
                        age_confirmed = st.button(
                            f'✔️ {m_name} Name mariyu Age nirdharinchandi',
                            key=f'confirm_age_btn_{idx}',
                            type='primary',
                        )
                        if age_confirmed:
                            st.session_state[is_confirmed_key] = True
                            trigger_rerun()
                    
                    if st.session_state.get(is_confirmed_key, False) or has_saved_before:
                        active_age = entered_age

                        if active_age > 70:
                            st.error("❌ Ee sabhyuralu 70 years datinanduna bimaku arhulru kadu.")
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

                            default_bank_val = str(current_row.get('BANK NAME', row.get('BANK NAME', ''))).strip().upper()
                            default_branch_val = str(current_row.get('BRANCH NAME', row.get('BRANCH NAME', ''))).strip().upper()
                            default_acc_val = str(current_row.get('MEMBER SB ACCOUNT NUMBER', row.get('MEMBER SB ACCOUNT NUMBER', ''))).strip()

                            bank_index = 0
                            if default_bank_val in all_available_banks:
                                bank_index = all_available_banks.index(default_bank_val)

                            entered_pmjjby_bank = default_bank_val
                            entered_pmsby_bank = default_bank_val
                            entered_pmjjby_branch = default_branch_val
                            entered_pmsby_branch = default_branch_val
                            entered_pmjjby_acc = default_acc_val
                            entered_pmsby_acc = default_acc_val

                            if 18 <= active_age <= 50:
                                st.markdown(
                                    '<div class="section-title-pmjjby">🛡 1. PMJJBY Scheme Details (18-50 yrs)</div>',
                                    unsafe_allow_html=True,
                                )
                                bc1, bc2, bc3 = st.columns(3)
                                with bc1:
                                    entered_pmjjby_bank = st.selectbox('PMJJBY Bank', all_available_banks, index=bank_index, key=f'pmjjby_bank_{idx}')
                                with bc2:
                                    available_pmjjby_branches = sorted(df[df['BANK NAME'] == entered_pmjjby_bank]['BRANCH NAME'].dropna().unique().tolist())
                                    if not available_pmjjby_branches:
                                        available_pmjjby_branches = [default_branch_val] if default_branch_val else ['MAIN BRANCH']
                                    
                                    branch_index_pm = 0
                                    if default_branch_val in available_pmjjby_branches:
                                        branch_index_pm = available_pmjjby_branches.index(default_branch_val)
                                    
                                    entered_pmjjby_branch = st.selectbox('PMJJBY Branch', available_pmjjby_branches, index=branch_index_pm, key=f'pmjjby_branch_{idx}')
                                with bc3:
                                    entered_pmjjby_acc = st.text_input('PMJJBY Acc No (Numbers only)', value=default_acc_val, key=f'pmjjby_acc_{idx}')

                                col_d1, col_d2 = st.columns(2)
                                with col_d1:
                                    pmjjby_sub_date = st.date_input('Application Submitted Date - PMJJBY (DD-MM-YYYY format)', value=existing_pm_sub, format="DD/MM/YYYY", key=f'pmjjby_sub_{idx}')
                                with col_d2:
                                    pmjjby_b_date = st.date_input('Bank Enrolled Date - PMJJBY (DD-MM-YYYY format)', value=existing_pm_bank, format="DD/MM/YYYY", key=f'pmjjby_b_opt_{idx}')

                            if 18 <= active_age <= 70:
                                st.markdown(
                                    '<div class="section-title-pmsby">🚑 2. PMSBY Scheme Details (18-70 yrs)</div>',
                                    unsafe_allow_html=True,
                                )
                                pc1, pc2, pc3 = st.columns(3)
                                with pc1:
                                    entered_pmsby_bank = st.selectbox('PMSBY Bank', all_available_banks, index=bank_index, key=f'pmsby_bank_{idx}')
                                with pc2:
                                    available_pmsby_branches = sorted(df[df['BANK NAME'] == entered_pmsby_bank]['BRANCH NAME'].dropna().unique().tolist())
                                    if not available_pmsby_branches:
                                        available_pmsby_branches = [default_branch_val] if default_branch_val else ['MAIN BRANCH']
                                    
                                    branch_index_ps = 0
                                    if default_branch_val in available_pmsby_branches:
                                        branch_index_ps = available_pmsby_branches.index(default_branch_val)
                                    
                                    entered_pmsby_branch = st.selectbox('PMSBY Branch', available_pmsby_branches, index=branch_index_ps, key=f'pmsby_branch_{idx}')
                                with pc3:
                                    entered_pmsby_acc = st.text_input('PMSBY Acc No (Numbers only)', value=default_acc_val, key=f'pmsby_acc_{idx}')

                                col_d3, col_d4 = st.columns(2)
                                with col_d3:
                                    pmsby_sub_date = st.date_input('Application Submitted Date - PMSBY (DD-MM-YYYY format)', value=existing_ps_sub, format="DD/MM/YYYY", key=f'pmsby_sub_{idx}')
                                with col_d4:
                                    pmsby_b_date_pmsby = st.date_input('Bank Enrolled Date - PMSBY (DD-MM-YYYY format)', value=existing_ps_bank, format="DD/MM/YYYY", key=f'pmsby_b_opt_{idx}')

                            if st.button(f'💾 {entered_name} Vivaralu Save Cheyandi', key=f'save_{idx}', type='primary'):
                                validation_error = False
                                
                                # Check Account Number contains only digits
                                active_acc_to_check = str(entered_pmjjby_acc).strip() if (18 <= active_age <= 50) else str(entered_pmsby_acc).strip()
                                if not active_acc_to_check.isdigit():
                                    validation_error = True
                                    st.error("❌ Account Number should contain only numbers (Digits only, no alphabets/special characters allowed)!")

                                if not validation_error and pmjjby_b_date and not pmjjby_sub_date:
                                    validation_error = True
                                    st.error("❌ PMJJBY lo: Munduga application submit date ivvakunda bank enroll date ivvakkudadu!")
                                
                                if not validation_error and pmsby_b_date_pmsby and not pmsby_sub_date:
                                    validation_error = True
                                    st.error("❌ PMSBY lo: Munduga application submit date ivvakunda bank enroll date ivvakkudadu!")

                                if not validation_error and pmjjby_sub_date and pmjjby_b_date:
                                    if pmjjby_b_date < pmjjby_sub_date:
                                        validation_error = True
                                        st.error("❌ PMJJBY lo: Bank enrolled date application submit date kante mundu undakudadu!")

                                if not validation_error and pmsby_sub_date and pmsby_b_date_pmsby:
                                    if pmsby_b_date_pmsby < pmsby_sub_date:
                                        validation_error = True
                                        st.error("❌ PMSBY lo: Bank enrolled date application submit date kante mundu undakudadu!")

                                if not validation_error:
                                    updated_row = row.to_dict()
                                    cleaned_new_name = str(entered_name).strip().upper()
                                    
                                    final_new_bank = str(entered_pmjjby_bank).strip().upper() if (18 <= active_age <= 50) else str(entered_pmsby_bank).strip().upper()
                                    final_new_branch = str(entered_pmjjby_branch).strip().upper() if (18 <= active_age <= 50) else str(entered_pmsby_branch).strip().upper()
                                    final_new_acc = str(entered_pmjjby_acc).strip() if (18 <= active_age <= 50) else str(entered_pmsby_acc).strip()

                                    updated_row['MEMBER NAME'] = cleaned_new_name
                                    updated_row['AGE'] = str(active_age)
                                    updated_row['BANK NAME'] = final_new_bank
                                    updated_row['BRANCH NAME'] = final_new_branch
                                    updated_row['MEMBER SB ACCOUNT NUMBER'] = final_new_acc
                                    
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

                                    active_scheme_name = 'PMJJBY' if (18 <= active_age <= 50 and (pmjjby_sub_date or pmjjby_b_date)) else ('PMSBY' if (18 <= active_age <= 70 and (pmsby_sub_date or pmsby_b_date_pmsby)) else ('PMJJBY' if 18 <= active_age <= 50 else 'PMSBY'))

                                    if final_new_bank != orig_bank:
                                        st.session_state.bank_corrections_log[m_id] = {
                                            'Mandal Name': str(row.get('MANDAL', '')),
                                            'VO Name': str(row.get('VO', '')),
                                            'SHG Name': str(row.get('SHG', '')),
                                            'Member Name': cleaned_new_name,
                                            'Member ID': str(m_id),
                                            'Scheme Name': active_scheme_name,
                                            'Old Bank Name': orig_bank,
                                            'New Bank Name': final_new_bank
                                        }
                                    elif m_id in st.session_state.bank_corrections_log:
                                        del st.session_state.bank_corrections_log[m_id]

                                    if final_new_acc != orig_acc:
                                        st.session_state.acc_corrections_log[m_id] = {
                                            'Mandal Name': str(row.get('MANDAL', '')),
                                            'VO Name': str(row.get('VO', '')),
                                            'SHG Name': str(row.get('SHG', '')),
                                            'Member Name': cleaned_new_name,
                                            'Member ID': str(m_id),
                                            'Scheme Name': active_scheme_name,
                                            'Old Bank Account Number': orig_acc,
                                            'New Bank Account Number': final_new_acc
                                        }
                                    elif m_id in st.session_state.acc_corrections_log:
                                        del st.session_state.acc_corrections_log[m_id]
                                    
                                    if pmjjby_sub_date: 
                                        updated_row[col_pmjjby_sub] = str(pmjjby_sub_date)
                                    if pmjjby_b_date: 
                                        updated_row[col_pmjjby_bank] = str(pmjjby_b_date)
                                    if pmsby_sub_date: 
                                        updated_row[col_pmsby_sub] = str(pmsby_sub_date)
                                    if pmsby_b_date_pmsby: 
                                        updated_row[col_pmsby_bank] = str(pmsby_b_date_pmsby)

                                    st.session_state.saved_entries_dict[m_id] = updated_row
                                    st.success(f'✅ {cleaned_new_name} vivaralu vijayavanthamga save cheyabaddayi!')
                                    trigger_rerun()

    elif app_mode == 'Mandal Wise':
        st.markdown("## 📍 Mandal Wise Summary")
        st.write('---')
        scheme_choice = st.radio('Scheme Enchukondi:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='m_scheme')

        mandal_summary = []
        for m_name, group in export_df_base.groupby('MANDAL'):
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

            mandal_summary.append({
                'Mandal Name': m_name, 'Target': target, 'Enrolled': enrolled,
                'Balance': balance, 'Applications Submitted': submitted, 'Yet to Submit': yet_to_submit
            })
        st.dataframe(pd.DataFrame(mandal_summary), use_container_width=True)

    elif app_mode == 'VO Wise':
        st.markdown("## 📊 VO Wise Summary")
        st.write('---')
        
        mandals_list = ['All Mandals'] + sorted(export_df_base['MANDAL'].dropna().unique().tolist())
        selected_mandal_filter = st.selectbox('Mandal Enchukondi:', mandals_list)
        scheme_choice = st.radio('Scheme Enchukondi:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='vo_scheme')
        
        filtered_df = export_df_base.copy()
        if selected_mandal_filter != 'All Mandals':
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

    elif app_mode == 'Bank Wise':
        st.markdown("## 🏛️ Bank Wise Summary")
        st.write('---')
        scheme_choice = st.radio('Scheme Enchukondi:', ['🛡️️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='bank_wise_scheme')

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

    elif app_mode == 'Branch Wise':
        st.markdown("## 📈 Branch Wise Summary")
        st.write('---')
        
        banks_list = ['All Banks'] + sorted(export_df_base['BANK NAME'].dropna().unique().tolist())
        selected_bank_filter = st.selectbox('Bank Enchukondi:', banks_list)
        scheme_choice = st.radio('Scheme Enchukondi:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True, key='b_scheme')

        filtered_bank_df = export_df_base.copy()
        if selected_bank_filter != 'All Banks':
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

    elif app_mode == 'Pending Reports':
        st.markdown("## 📥 Pending Reports")
        st.write('---')

        report_type = st.selectbox(
            'Report Type Enchukondi:',
            [
                '1. Enrolled List',
                '2. Submitted & Pending at Bank',
                '3. Yet to Submit to Bank'
            ]
        )

        scheme_filter = st.radio('Scheme Enchukondi:', ['🛡️ PMJJBY', '🚑 PMSBY'], horizontal=True)
        is_pmjjby = (scheme_filter == '🛡️ PMJJBY')

        area_scope = st.radio('Scope Enchukondi:', ['Entire District', 'Specific Mandal'], horizontal=True)

        target_df = export_df_base.copy()
        if area_scope == 'Specific Mandal':
            mandals_list_det = sorted(target_df['MANDAL'].dropna().unique().tolist())
            chosen_mandal = st.selectbox('Mandal Enchukondi:', mandals_list_det)
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

        st.markdown(f'### 📋 Members List (Total: {len(result_list)})')

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
                label='📥 Download Report as CSV',
                data=csv_data,
                file_name=f'Insurance_Report_{report_type[:3]}_{scheme_filter[2:]}.csv',
                mime='text/css',
                type='primary'
            )
        else:
            st.info('👉 Ee filter ku saripoye records emi levu.')

    elif app_mode == 'Member Level':
        st.markdown("## 👥 Complete Members List")
        st.write('---')
        selected_mandal_filter = st.selectbox('Mandal filter:', ['All'] + sorted(export_df_base['MANDAL'].dropna().unique().tolist()))
        
        filtered_report_df = export_df_base.copy()
        if selected_mandal_filter != 'All':
            filtered_report_df = filtered_report_df[filtered_report_df['MANDAL'] == selected_mandal_filter]

        st.dataframe(filtered_report_df[['MANDAL', 'VO', 'SHG', 'MEMBER NAME', 'MEMBER ID', 'AGE', col_pmjjby_sub, col_pmjjby_bank, col_pmsby_sub, col_pmsby_bank]], use_container_width=True)

    elif app_mode == 'Corrections Reports':
        st.markdown("## 📝 Corrections Report")
        st.write('---')

        correction_type = st.selectbox(
            'Report Type Enchukondi:',
            [
                '1. ✏️ Name Corrections',
                '2. 🔢 Age Corrections',
                '3. 🏛️️ Bank Name Corrections',
                '4. 💳 Account Number Corrections'
            ]
        )

        if '1.' in correction_type:
            st.markdown("### ✏️ Name Corrections Report")
            if len(st.session_state.name_corrections_log) > 0:
                name_corr_df = pd.DataFrame(list(st.session_state.name_corrections_log.values()))
                
                mandal_list_nc = ['All'] + sorted(name_corr_df['Mandal Name'].dropna().unique().tolist())
                chosen_m_nc = st.selectbox('Mandal filter:', mandal_list_nc, key='nc_mandal_filter')
                
                if chosen_m_nc != 'All':
                    name_corr_df = name_corr_df[name_corr_df['Mandal Name'] == chosen_m_nc]
                
                st.markdown(f'📋 **Total Name Corrections:** {len(name_corr_df)}')
                st.dataframe(name_corr_df[['Mandal Name', 'VO Name', 'SHG Name', 'Member Name', 'Member ID', 'Corrected Name']], use_container_width=True)
                
                csv_nc = name_corr_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Download Name Corrections CSV',
                    data=csv_nc,
                    file_name='Name_Corrections_Report.csv',
                    mime='text/css',
                    type='primary'
                )
            else:
                st.info('👉 Ippativaraku elanti name corrections namodu cheyabadaledu.')

        elif '2.' in correction_type:
            st.markdown("### 🔢 Age Corrections Report")
            if len(st.session_state.age_corrections_log) > 0:
                age_corr_df = pd.DataFrame(list(st.session_state.age_corrections_log.values()))
                
                mandal_list_ac = ['All'] + sorted(age_corr_df['Mandal Name'].dropna().unique().tolist())
                chosen_m_ac = st.selectbox('Mandal filter:', mandal_list_ac, key='ac_mandal_filter')
                
                if chosen_m_ac != 'All':
                    age_corr_df = age_corr_df[age_corr_df['Mandal Name'] == chosen_m_ac]
                
                st.markdown(f'📋 **Total Age Corrections:** {len(age_corr_df)}')
                st.dataframe(age_corr_df[['Mandal Name', 'VO Name', 'SHG Name', 'Member Name', 'Member ID', 'Old Age', 'New Age']], use_container_width=True)
                
                csv_ac = age_corr_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Download Age Corrections CSV',
                    data=csv_ac,
                    file_name='Age_Corrections_Report.csv',
                    mime='text/css',
                    type='primary'
                )
            else:
                st.info('👉 Ippativaraku elanti age corrections namodu cheyabadaledu.')

        elif '3.' in correction_type:
            st.markdown("### 🏛️ Bank Name Corrections Report")
            if len(st.session_state.bank_corrections_log) > 0:
                bank_corr_df = pd.DataFrame(list(st.session_state.bank_corrections_log.values()))
                
                mandal_list_bc = ['All'] + sorted(bank_corr_df['Mandal Name'].dropna().unique().tolist())
                chosen_m_bc = st.selectbox('Mandal filter:', mandal_list_bc, key='bc_mandal_filter')
                
                if chosen_m_bc != 'All':
                    bank_corr_df = bank_corr_df[bank_corr_df['Mandal Name'] == chosen_m_bc]
                
                st.markdown(f'📋 **Total Bank Name Corrections:** {len(bank_corr_df)}')
                st.dataframe(bank_corr_df[['Mandal Name', 'VO Name', 'SHG Name', 'Member Name', 'Member ID', 'Scheme Name', 'Old Bank Name', 'New Bank Name']], use_container_width=True)
                
                csv_bc = bank_corr_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Download Bank Corrections CSV',
                    data=csv_bc,
                    file_name='Bank_Name_Corrections_Report.csv',
                    mime='text/css',
                    type='primary'
                )
            else:
                st.info('👉 Ippativaraku elanti bank name corrections namodu cheyabadaledu.')

        elif '4.' in correction_type:
            st.markdown("### 💳 Account Number Corrections Report")
            if len(st.session_state.acc_corrections_log) > 0:
                acc_corr_df = pd.DataFrame(list(st.session_state.acc_corrections_log.values()))
                
                mandal_list_acc = ['All'] + sorted(acc_corr_df['Mandal Name'].dropna().unique().tolist())
                chosen_m_acc = st.selectbox('Mandal filter:', mandal_list_acc, key='acc_mandal_filter')
                
                if chosen_m_acc != 'All':
                    acc_corr_df = acc_corr_df[acc_corr_df['Mandal Name'] == chosen_m_acc]
                
                st.markdown(f'📋 **Total Account Number Corrections:** {len(acc_corr_df)}')
                st.dataframe(acc_corr_df[['Mandal Name', 'VO Name', 'SHG Name', 'Member Name', 'Member ID', 'Scheme Name', 'Old Bank Account Number', 'New Bank Account Number']], use_container_width=True)
                
                csv_acc = acc_corr_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='📥 Download Account Number Corrections CSV',
                    data=csv_acc,
                    file_name='Account_Number_Corrections_Report.csv',
                    mime='text/css',
                    type='primary'
                )
            else:
                st.info('👉 Ippativaraku elanti account number corrections namodu cheyabadaledu.')
