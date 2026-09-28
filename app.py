st.sidebar.header("📁 నావిగేషన్")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 రిపోర్ట్‌లు డౌన్‌లోడ్")

    # 1. నమోదు చేసిన వివరాలు (Already Entered)
    report_df = export_df_base[
        export_df_base[col_pmjjby_sub].notna() | 
        export_df_base[col_pmjjby_bank].notna() | 
        export_df_base[col_pmsby_sub].notna() | 
        export_df_base[col_pmsby_bank].notna()
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
        's.no', 'MANDAL', 'VO', 'SHG', 'MEMBER NAME', 'MEMBER ID', 'AGE', 
        'BANK NAME', 'BRANCH NAME', 'MEMBER SB ACCOUNT NUMBER', 
        'Application Submitted at Bank - PMJJBY', 'Bank Enrolled Date - PMJJBY', 
        'Application Submitted at Bank - PMSBY', 'Bank Enrolled Date - PMSBY', 'age correction'
    ]

    final_columns = [c for c in desired_columns if c in export_df.columns]
    export_df = export_df[final_columns]

    entered_csv_report = export_df.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button(
        label="📥 1. నమోదు చేసిన వివరాలు (Entered)",
        data=entered_csv_report,
        file_name="Enrolled_Members_Report.csv",
        mime="text/csv",
        use_container_width=True
    )

    # -------------------------------------------------------------
    # 2. Scheme Wise Done & Pending Filtering Logic
    # -------------------------------------------------------------
    # Helper to clean AGE column for filtering
    temp_df = export_df_base.copy()
    temp_df['NUM_AGE'] = pd.to_numeric(temp_df['AGE'], errors='coerce').fillna(0)

    # A. PMJJBY Done
    pmjjby_done_df = temp_df[
        temp_df[col_pmjjby_sub].notna() | temp_df[col_pmjjby_bank].notna()
    ]
    pmjjby_done_csv = pmjjby_done_df.to_csv(index=False).encode('utf-8-sig')

    # B. PMJJBY Pending (Age 18 to 50 & Not Done)
    pmjjby_pending_df = temp_df[
        (temp_df['NUM_AGE'] >= 18) & (temp_df['NUM_AGE'] <= 50) &
        (temp_df[col_pmjjby_sub].isna()) & (temp_df[col_pmjjby_bank].isna())
    ]
    pmjjby_pending_csv = pmjjby_pending_df.to_csv(index=False).encode('utf-8-sig')

    # C. PMSBY Done
    pmsby_done_df = temp_df[
        temp_df[col_pmsby_sub].notna() | temp_df[col_pmsby_bank].notna()
    ]
    pmsby_done_csv = pmsby_done_df.to_csv(index=False).encode('utf-8-sig')

    # D. PMSBY Pending (Age 18 to 70 & Not Done)
    pmsby_pending_df = temp_df[
        (temp_df['NUM_AGE'] >= 18) & (temp_df['NUM_AGE'] <= 70) &
        (temp_df[col_pmsby_sub].isna()) & (temp_df[col_pmsby_bank].isna())
    ]
    pmsby_pending_csv = pmsby_pending_df.to_csv(index=False).encode('utf-8-sig')

    # -------------------------------------------------------------
    # Sidebar Dropdown / Expanders for Downloads
    # -------------------------------------------------------------
    with st.sidebar.expander("🛡️ PMJJBY రిపోర్ట్‌లు"):
        st.download_button(
            label="✅ PMJJBY చేసినవి (Done)",
            data=pmjjby_done_csv,
            file_name="PMJJBY_Done_Report.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.download_button(
            label="⏳ PMJJBY చేయవలసినవి (Pending)",
            data=pmjjby_pending_csv,
            file_name="PMJJBY_Pending_Report.csv",
            mime="text/csv",
            use_container_width=True
        )

    with st.sidebar.expander("🚑 PMSBY రిపోర్ట్‌లు"):
        st.download_button(
            label="✅ PMSBY చేసినవి (Done)",
            data=pmsby_done_csv,
            file_name="PMSBY_Done_Report.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.download_button(
            label="⏳ PMSBY చేయవలసినవి (Pending)",
            data=pmsby_pending_csv,
            file_name="PMSBY_Pending_Report.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.sidebar.markdown("---")
