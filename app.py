import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Authentication
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
gc = gspread.authorize(creds)

# Load Google Sheet
def load_sheet(sheet_url, worksheet_name):
    sh = gc.open_by_url(sheet_url)
    worksheet = sh.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    return pd.DataFrame(data), worksheet

# Update Google Sheet
def update_sheet(worksheet, df):
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

# Streamlit App
st.title("📌 Project Management Dashboard")

# Google Sheets Details
SHEET_URL = "YOUR_GOOGLE_SHEET_URL"
WORKSHEET_NAME = "Sheet1"

df, worksheet = load_sheet(SHEET_URL, WORKSHEET_NAME)

# Display Table with Checkbox
for index, row in df.iterrows():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"### {row['Task Name']}")
        st.write(f"📅 Due Date: {row['Due Date']}")
    with col2:
        done = st.checkbox("Done", value=(row['Status'] == "Done"), key=index)
        df.at[index, 'Status'] = "Done" if done else "Not Done"

# Save Button
if st.button("Save Changes"):
    update_sheet(worksheet, df)
    st.success("✅ Updates saved successfully!")



    
