import pandas as pd
import requests
import gspread

def get_disruptions_data(septa_disruptions_url):
    try:
        if septa_disruptions_url == '':
            raise Exception('Provided URL is an empty string.')
        
        response = requests.get(septa_disruptions_url)

        response.raise_for_status()

        septa_disruptions_json = response.json()

        septa_disruptions_df = pd.DataFrame(septa_disruptions_json)
        septa_disruptions_df[['detour_start_date_time', 'detour_end_date_time']] = septa_disruptions_df[['detour_start_date_time', 'detour_end_date_time']].astype('datetime64')
        
        if septa_disruptions_df.shape[0] < 100:
            raise Exception('There\'s less than 100 disruptions, normally the url has over 200')

        return septa_disruptions_df

    except requests.HTTPError as http_error:
        print(f'Failed response: Code: {http_error}')
        raise http_error

    except requests.ConnectionError as connection_error:
        print(f'No Connection, the website doesn\'t exist: {connection_error}')
        raise connection_error

    except Exception as unexpected_error:
        print(f'Unexprected Error: {unexpected_error}')
        raise unexpected_error

def get_google_worksheets(spreadsheet_name,credentials_filename='../credentials.json'):
    
    google_sheet = gspread.service_account(filename=credentials_filename).open(spreadsheet_name)

    return {str(worksheet.title): worksheet for worksheet in google_sheet.worksheets()}
