import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_google():
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file('supernova-394405-a398b70d278d.json', scopes=scopes)
        gc = gspread.authorize(credentials)
        gauth = GoogleAuth()
        drive = GoogleDrive(gauth)

        return gc

    except Exception as e:
        raise Exception(f"Error authenticating with Google: {e}")

def load_data_to_sheet(google_sheet_lis, report_sheet_lis):
    try:
        gc = authenticate_google()

        for gsheet, reportsheet in zip(google_sheet_lis, report_sheet_lis):
            # Open a Google Sheet
            gs = gc.open_by_key('1M0EZqJZSk5LxLarS7zzA4vs17QUiYlwIxrk-o5M0Jzs')

            # Select a worksheet from its name
            worksheet = gs.worksheet(gsheet)

            # Read data from CSV file into DataFrame
            df = pd.read_csv('./reports/' + reportsheet)

            # Write DataFrame to the worksheet
            worksheet.clear()
            set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=False, include_column_header=True,
                               resize=True)
            print(f'Data Loaded in {gsheet} sheet')

    except Exception as e:
        print(f"Error loading data to the sheet: {e}")

