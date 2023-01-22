from gspread_dataframe import set_with_dataframe

from connections import get_disruptions_data, get_google_worksheets
from scraper import *

def main():
    raw_df = get_disruptions_data('http://www3.septa.org/hackathon/Alerts/get_alert_data.php?req1=all')
    filtered_rows_and_columns_df = filter_rows_and_columns(raw_df)
    separated_advisories_df = separate_advisories_attached_to_detours_into_new_df(filtered_rows_and_columns_df)
    split_advisories_df = split_advisories_into_new_df(filtered_rows_and_columns_df)
    concated_advisories_df = concat_separated_advisories_df_and_split_advisories_df(separated_advisories_df, split_advisories_df)
    final_advisories_df = clean_concated_advisories_df(concated_advisories_df)
    detours_df = separate_detours_into_new_df(filtered_rows_and_columns_df)
    title_column = detours_df.apply(create_title_column, axis=1).copy(deep=True)
    description_column = detours_df.apply(create_description_column, axis=1).copy(deep=True)

    detour_df_columns = {
        'Line': detours_df['route_name'], 
        'Title': title_column, 
        'Description': description_column, 
        'Detour Reason': detours_df['detour_reason'],
        'Type': 'Detour',
        'Start Date': detours_df['detour_start_date_time'],
        'End Date': detours_df['detour_end_date_time']
    }

    final_detours_df = pd.DataFrame(detour_df_columns)
    final_df = concat_final_advisories_df_to_final_detours_df(final_detours_df, final_advisories_df)

    sheets = get_google_worksheets('json_scrape', '../docs/credentials.json')
    set_with_dataframe(sheets['Sheet1'], final_df)

if __name__ == '__main__':
    main()