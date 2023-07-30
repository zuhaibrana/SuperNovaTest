import pandas as pd
import requests
from credentials import endpoints 
import requests


def GetURL(api):
    url = endpoints.get(api)
    return url


def Get_User_Comments(api):
    try:
        # Get the URL for the API endpoint
        url = GetURL(api)
        
        #  Make a GET request to the API
        response = requests.get(url)
        
        # Check if the API request was successful (status code 2xx)
        response.raise_for_status()  # Raise an error if the API request fails

        #  Convert the API response to JSON format
        data = response.json()
        
        # Convert the API name to lowercase for DataFrame column naming consistency
        api = api.lower()

        #  Normalize the JSON data and create a DataFrame
        df = pd.json_normalize(data[api])
        
        #  Remove any dots in the column names (for better handling of nested data)
        df.columns = df.columns.str.replace('.', '')

        #  Use a context manager for file writing to handle resources properly
        with open('./rawdata/'+api + '.csv', 'w', newline='', encoding='utf-8') as file:
            df.to_csv(file, index=False)
            
        # extract users address details    
        if api == 'users':
            df_users_add = df[['id','addressaddress','addresscity','addresscoordinateslat','addresscoordinateslng','addresspostalCode','addressstate']]
            
            #  Use a context manager for file writing to handle resources properly
            with open('./rawdata/'+api +'_address' +'.csv', 'w', newline='', encoding='utf-8') as file:
                df_users_add.to_csv(file, index=False)
                
        #  Print a success message after saving the DataFrame to CSV
        print(f"Successfully saved {api}.csv")

        
    except requests.exceptions.RequestException as e:
        # Error handling for API request exceptions
        print(f"Error occurred while making the API request: {e}")
        
    except KeyError as e:
        # Error handling for missing keys in the API response
        print(f"Key '{api}' not found in the API response data: {e}")

    except Exception as e:
        # Error handling for unexpected exceptions
        print(f"An unexpected error occurred: {e}")


def GetCarts(api):
    try:
        #  Get the URL for the API endpoint
        url = GetURL(api)
        
        #  Make a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the API request fails

        #  Convert the API response to JSON format
        data = response.json()
        
        # Define column names for the DataFrame
        columnNames = ['carts_id', 'carts_total', 'carts_discountedTotal', 'carts_userId', 'carts_totalProducts', 'carts_totalQuantity',
                       'product_id', 'product_title', 'product_product_price', 'product_quantity', 'product_total',
                       'product_discountedPercentage', 'product_discountedPrice']
        
        #  Convert the API name to lowercase for DataFrame column naming consistency
        api = api.lower()

        #  Create an empty DataFrame with specified column names
        df = pd.DataFrame(columns=columnNames)
        
        #  Iterate through the API response and populate the DataFrame
        for i in range(0, len(data[api])):
            tmp_lis = []
            tmp_lis.append(data[api][i]['id'])
            tmp_lis.append(data[api][i]['total'])
            tmp_lis.append(data[api][i]['discountedTotal'])
            tmp_lis.append(data[api][i]['userId'])
            tmp_lis.append(data[api][i]['totalProducts'])
            tmp_lis.append(data[api][i]['totalQuantity'])

            for j in range(0, len(data['carts'][0]['products'])):
                tmp_lis2 = list(data['carts'][i]['products'][j].values())

                final = tmp_lis + tmp_lis2
                df.loc[len(df)] = final
        
        #  Use a context manager for file writing to handle resources properly
        with open('./rawdata/'+api + '.csv', 'w', newline='', encoding='utf-8') as file:
            df.to_csv(file, index=False)

        #  Print a success message after saving the DataFrame to CSV
        print(f"Successfully saved {api}.csv")
        
    except requests.exceptions.RequestException as e:
        # Error handling for API request exceptions
        print(f"Error occurred while making the API request: {e}")
        
    except KeyError as e:
        # Error handling for missing keys in the API response
        print(f"Key '{api}' not found in the API response data: {e}")

    except Exception as e:
        # Error handling for unexpected exceptions
        print(f"An unexpected error occurred: {e}")


def get_Products_Posts(api):
    try:
        #  Get the URL for the API endpoint
        url = GetURL(api)
        
        #  Make a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the API request fails

        #  Convert the API response to JSON format
        data = response.json()
        
        #  Convert the API name to lowercase for DataFrame column naming consistency
        api = api.lower()

        #  Normalize the JSON data and create a DataFrame
        df = pd.json_normalize(data[api])
        
        # Define functions to split lists into separate columns
        def split_images(row):
            return pd.Series(row['images'])
        
        def split_tags(row):
            return pd.Series(row['tags'])
        
        # Check if the API is 'products' or 'posts' and process accordingly
        if api == 'products':
            # Split images into separate columns
            df[['image1', 'image2', 'image3', 'image4', 'image5', 'image6']] = df.apply(split_images, axis=1)
            df.drop(['images'], axis=1, inplace=True)
            df.fillna('NULL', inplace=True)
            
        else:
            # Split tags into separate columns
            df[['tag1', 'tag2', 'tag3']] = df.apply(split_tags, axis=1)
            df.drop(['tags'], axis=1, inplace=True)
            df.fillna('NULL', inplace=True)
        
        #  Use a context manager for file writing to handle resources properly
        with open('./rawdata/'+api + '.csv', 'w', newline='', encoding='utf-8') as file:
            df.to_csv(file, index=False)

        #  Print a success message after saving the DataFrame to CSV
        print(f"Successfully saved {api}.csv")
        
    except requests.exceptions.RequestException as e:
        # Error handling for API request exceptions
        print(f"Error occurred while making the API request: {e}")
        
    except KeyError as e:
        # Error handling for missing keys in the API response
        print(f"Key '{api}' not found in the API response data: {e}")

    except Exception as e:
        # Error handling for unexpected exceptions
        print(f"An unexpected error occurred: {e}")

