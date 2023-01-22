import re
from datetime import date, timedelta

import pandas as pd
from bs4 import BeautifulSoup

# drops rows where detour_message is None and advisory_message is None or route_id doesn't start with b or t
def filter_rows_and_columns(df: pd.DataFrame) -> pd.DataFrame:
    filtered_nulls_df = df.dropna(subset=['detour_message', 'advisory_message'], how='all')
    filtered_bus_and_trolley_df = filtered_nulls_df[
        (filtered_nulls_df['route_id'].str.startswith('b')) | 
        (filtered_nulls_df['route_id'].str.startswith('t'))
    ]
    return filtered_bus_and_trolley_df.drop([
        'route_id', 'current_message', 'advisory_id', 'detour_id', 'last_updated', 'isSnow'], axis=1)

# creates a dataframe of the advisories that are in the same row as a detour
# drops duplicates that occur due to multiple route detours
# sets all detour related columns to None
def separate_advisories_attached_to_detours_into_new_df(df: pd.DataFrame) -> pd.DataFrame:
    separated_advisories_df = df[(df['advisory_message'].notnull()) & (df['detour_message'].notnull())].copy(deep=True)
    separated_advisories_df.drop_duplicates(subset=['route_name', 'advisory_message'], inplace=True)
    separated_advisories_df[['detour_message', 'detour_start_location', 'detour_start_date_time', 'detour_end_date_time', 'detour_reason']] = None
    return separated_advisories_df

# takes rows that have an advisory message and no detour message and makes a df
# sets all detour related columns to None
def split_advisories_into_new_df(df: pd.DataFrame) -> pd.DataFrame:
    split_advisories_df = df[(df['advisory_message'].notnull()) & (df['detour_message'].isnull())].copy(deep=True)
    split_advisories_df[['detour_start_location', 'detour_start_date_time', 'detour_end_date_time', 'detour_reason']] = None
    return split_advisories_df

def concat_separated_advisories_df_and_split_advisories_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2], ignore_index=True)

def clean_concated_advisories_df(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_advisories = []
    for _, row in df.iterrows():
        soup = BeautifulSoup(row['advisory_message'], 'lxml')
        advisory_titles = soup.find_all('h3', class_='separated')
        advisories = []

        for advisory in advisory_titles:
            descriptions = []
            advisory_information = {
                'Line': row['route_name'],
                'Title': advisory.get_text(),
                'Detour Reason': None,
                'Type': 'Advisory'
            }
            for i, elem in enumerate(advisory.next_siblings):
                if elem.name == 'h3':
                    break
                elif elem.name == 'p':
                    if i == 0:
                        until_further_notice = re.search('until further notice', elem.get_text(), flags=re.I)
                        if until_further_notice: 
                            advisory_information['End Date'] = elem.get_text()
                            advisory_information['Start Date'] = None
                        else:
                            advisory_information['Start Date'] = elem.get_text()
                    else:
                        descriptions.append(elem.get_text())

            advisory_information['Description'] = ' '.join(descriptions)
            advisories.append(advisory_information)
        
        cleaned_advisories += advisories

    cleaned_advisories_df = pd.DataFrame(cleaned_advisories)
    cleaned_advisories_df = cleaned_advisories_df[['Line', 'Title', 'Description', 'Detour Reason', 'Type', 'Start Date', 'End Date']]
    return cleaned_advisories_df

def separate_detours_into_new_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['detour_message'].notnull() & (pd.to_datetime(df['detour_end_date_time']).dt.date >= date.today() + timedelta(days=3))].reset_index(drop=True)
    return df.drop(['advisory_message'], axis=1)

def create_title_column(row: pd.DataFrame) -> str:
    title = str(row['detour_start_location'])

    replacements = [
       (r'\s{2,}', ' '),
       (r' Sts\.?', '')
    ]
    
    for old, new in replacements:
        title = re.sub(old, new, title, flags=re.I)

    return title + ', Detour'

def create_description_column(row: pd.DataFrame) -> str:
    description = str(row['detour_message'])

    replacements = [
       (r'\s*,\s*', ' '),
       (r'\s{2,}', ' '),
       (r',*\s*Right on', ', R -'),
       (r',*\s*Left on', ', L -'),
       (r',*\s*reg (rte?|route)?', ', Reg Rte')
    ]

    for old, new in replacements:
        description = re.sub(old, new, description, flags=re.I)

    return description

def concat_final_advisories_df_to_final_detours_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([df1, df2])

