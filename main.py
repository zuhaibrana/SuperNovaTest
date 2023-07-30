
from src.api_data import Get_User_Comments , GetCarts, get_Products_Posts
#from src.gen_reports import GenerateReports
from src.load_google_sheet import load_data_to_sheet
from src.create_chart import create_bar_chart

from credentials import sheetinfo
import warnings

# STEP 1
def extract_data():
    try:
        # Data extraction part in the rawdata folder

        # Using same function for api users and comment as have same dict format.
        # also extracting user address from users api data.
        Get_User_Comments('USERS')
        Get_User_Comments('COMMENTS')
        GetCarts('CARTS')
        # Using same function for api products and posts as have same list format.
        get_Products_Posts('PRODUCTS')
        # enabling the tags to keep seprate file and extraction
        get_Products_Posts('POSTS')
        
    except Exception as e:
        print(f"Error occurred during data extraction: {e}")



# STEP 2
#For db creating a database on https://www.db4free.net also attched the db credentials to review.



#STEP 3
def GenerateReports():
    try:
    	# runs sql query on the sql server and save response in csv fomrat.
        GenerateReports()
        
    except Exception as e:
        print(f"Error occurred during reports processing: {e}")


def load_data_to_google_sheet():
    try:
    	# load csv reports data to google sheet via api
        google_sheet_lis = ['Report1', 'Report2', 'Report3']
        report_sheet_lis = ['q1_response.csv', 'q2_response.csv', 'q3_response.csv']
        load_data_to_sheet(google_sheet_lis, report_sheet_lis)
        
    except Exception as e:
        print(f"Error occurred during loading data to Google Sheet: {e}")


# STEP 4
def CreateReportGraph():
    try:
    	google_sheet_lis = ['Report1', 'Report2', 'Report3']
    	report_sheet_lis = ['q1_response.csv', 'q2_response.csv', 'q3_response.csv']

    	load_data_to_sheet(google_sheet_lis, report_sheet_lis)
        
    except Exception as e:
        print(f"Error occurred during chart cretion to Google Sheet: {e}")


def main():
    warnings.filterwarnings("ignore")
    
    # STEP 1: Extract data from APIs and save to rawdata folder
    extract_data()

    # STEP 2: Create and update the database on https://www.db4free.net
    # Database credentials to be reviewed.

    # STEP 3: Run SQL queries on the server and save the response in CSV format
    try:
        #GenerateReports()
    	load_data_to_google_sheet()
    except Exception as e:
        print(f"Error occurred during data extraction: {e}")

    
    # STEP 4: Insert a bar chart using the total revenue generated per state
    sheet_id = sheetinfo.get('SHEETID')
    sheet_name = sheetinfo.get('SHEETNAME')
    create_bar_chart(sheet_id, sheet_name)

if __name__ == "__main__":
    main()