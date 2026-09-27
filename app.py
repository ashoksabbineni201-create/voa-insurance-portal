import pandas as pd
import streamlit as st

# VOA ఎంట్రీలు మరియు అప్‌డేటెడ్ వివరాలతో కూడిన డేటాను ఎక్సెల్/CSV రూపంలో డౌన్‌లోడ్ చేసుకునే బటన్ కోడ్:

st.markdown(
    '### 📥 VOA ఎంట్రీల రిపోర్ట్ డౌన్‌లోడ్'
)  # VOA entry report download heading
st.write(
    'యాప్‌లో VOAలు ఎంటర్ చేసిన మరియు అప్‌డేట్ చేసిన పూర్తి వివరాలను ఇక్కడ CSV'
    ' ఫైల్ రూపంలో డౌన్‌లోడ్ చేసుకోవచ్చు.'
)

# ఉదాహరణకు మీ వద్ద ఉన్న ఫిల్టర్ చేసిన మెంబర్స్ డేటాను DataFrame రూపంలో తీసుకుని CSV గా మార్చవచ్చు:
if 'members_df' in locals() and not members_df.empty:
  # డేటాను CSV కి కన్వర్ట్ చేయడం
  csv_report = members_df.to_csv(index=False).encode('utf-8')

  st.download_button(
    label='📥 VOA ఎంట్రీల డేటాను డౌన్‌లోడ్ చేసుకోండి (CSV)',
    data=csv_report,
    file_name='VOA_Enrollment_Entries_Report.csv',
    mime='text/csv',
  )
else:
  st.info(
    'దయచేసి ముందుగా మండలం, VO మరియు SHG గ్రూప్‌ను ఎంచుకోండి, అప్పుడు ఆ గ్రూప్'
    ' మెంబర్ల డేటా డౌన్‌లోడ్ బటన్ కనిపిస్తుంది.'
  )
