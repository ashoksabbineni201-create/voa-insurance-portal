# CSV Export కోసం DataFrame సిద్ధం చేయడం
  export_df = report_df.copy()

  # కాలమ్స్ రీనేమ్ చేయడం
  rename_dict = {
      col_pmjjby_sub: 'Application Submitted at Bank - PMJJBY',
      col_pmsby_sub: 'Application Submitted at Bank - PMSBY',
      col_pmjjby_bank: 'Bank Enrolled Date - PMJJBY',
      col_pmsby_bank: 'Bank Enrolled Date - PMSBY',
  }
  export_df = export_df.rename(columns=rename_dict)

  # S.No మరియు Age Correction అమర్చడం
  if 's.no' not in export_df.columns and not export_df.empty:
    export_df.insert(0, 's.no', range(1, len(export_df) + 1))

  if 'AGE' in export_df.columns:
    export_df['age correction'] = export_df['AGE']

  # కావాల్సిన నిర్దిష్ట కాలమ్స్‌ను మాత్రమే ఎంచుకోవడం (అనవసరమైన తెలుగు కాలమ్స్ తీసివేయుటకు)
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

  # ఉన్న కాలమ్స్ మాత్రమే ఫిల్టర్ చేయడం
  final_columns = [c for c in desired_columns if c in export_df.columns]
  export_df = export_df[final_columns]

  # Excel లో తెలుగు ఫాంట్ సరిగ్గా కనిపించడానికి utf-8-sig ఎన్‌కోడింగ్ ఉపయోగించడం
  entered_csv_report = export_df.to_csv(index=False).encode('utf-8-sig')

  st.sidebar.download_button(
      label='📥 ఎంట్రీ చేసిన వివరాలు మాత్రమే డౌన్‌లోడ్ చేసుకోండి (CSV)',
      data=entered_csv_report,
      file_name='Enrolled_Members_Report.csv',
      mime='text/csv',
  )
