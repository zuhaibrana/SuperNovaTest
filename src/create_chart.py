import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from credentials import sheetinfo


def create_bar_chart(sheet_id, sheet_name):
    # Load credentials from the JSON file
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('supernova-394405-a398b70d278d.json', scope)
    
    # Authorize the client
    client = gspread.authorize(credentials)
    
    # Open the specified spreadsheet
    spreadsheet = client.open_by_key(sheet_id)
    
    # Select the sheet to work with
    sheet = spreadsheet.worksheet(sheet_name)
    
    # Get the data from the sheet
    data = sheet.get_all_values()
    
    # Prepare data for the chart
    labels = [row[0] for row in data[1:]]  # Ignore the header row
    ages = [int(row[1]) for row in data[1:]]  # Ignore the header row
    
    # Build the Google Sheets API service
    service = build('sheets', 'v4', credentials=credentials)
    
    # Create the chart data
    chart_data = {
        "spec": {
            "title": "Age Distribution",
            "basicChart": {
                "chartType": "BAR",
                "legendPosition": "RIGHT_LEGEND",
                "axis": [
                    {
                        "position": "BOTTOM_AXIS",
                        "title": "Name",
                        "format": {
                            "textFormat": {
                                "fontSize": 10
                            }
                        }
                    },
                    {
                        "position": "LEFT_AXIS",
                        "title": "Age",
                        "format": {
                            "textFormat": {
                                "fontSize": 10
                            }
                        }
                    }
                ],
                "domains": [
                    {
                        "domain": {
                            "sourceRange": {
                                "sources": [
                                    {
                                        "sheetId": sheet._properties['sheetId'],
                                        "startRowIndex": 1,
                                        "endRowIndex": len(labels) + 1,
                                        "startColumnIndex": 1,
                                        "endColumnIndex": 2
                                    }
                                ]
                            }
                        }
                    }
                ],
                "series": [
                    {
                        "series": {
                            "sourceRange": {
                                "sources": [
                                    {
                                        "sheetId": sheet._properties['sheetId'],
                                        "startRowIndex": 1,
                                        "endRowIndex": len(ages) + 1,
                                        "startColumnIndex": 2,
                                        "endColumnIndex": 3
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        }
    }
    
    # Add the chart to the sheet
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={
            "requests": [
                {
                    "addChartEx": {
                        "chart": chart_data,
                        "position": {
                            "overlayPosition": {
                                "sheetId": sheet._properties['sheetId']
                            }
                        }
                    }
                }
            ]
        }
    ).execute()
    

