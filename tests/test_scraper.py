import pandas as pd

import philly_scrape.scraper as scraper

def create_data_frame(**columns_and_data_points):
    return pd.DataFrame(data=columns_and_data_points)

class TestFilterRowsAndColumns():
    def test_detour_message_is_none_and_advisory_message_is_none_returns_empty_dataframe(self):
        test_df = scraper.filter_rows_and_columns(
            create_data_frame(
                route_id = ['b'],
                route_name = ['1'],
                current_message = ['test'],
                advisory_id = ['test'], 
                advisory_message = [None],
                detour_message = [None],
                detour_id = ['test'],
                detour_start_location = ['test'], 
                detour_start_date_time = ['test'],
                detour_end_date_time = ['test'], 
                detour_reason = ['test'],
                last_updated = ['test'],
                isSnow = ['test']))
        
        expected_df = create_data_frame(
                            route_name = [], 
                            advisory_message = [], 
                            detour_message = [],
                            detour_start_location = [],
                            detour_start_date_time = [],
                            detour_end_date_time = [],
                            detour_reason = [])
        
        pd.testing.assert_frame_equal(test_df, expected_df, check_dtype=False)

    def test_route_id_starting_with_letter_other_than_b_or_t_returns_empty_dataframe(self):
        data_points = ['test'] * 24

        test_df = scraper.filter_rows_and_columns(
            create_data_frame(
                route_id = ['a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                            'n', 'o', 'p', 'q', 'r', 's', 'u', 'v', 'w', 'x', 'y', 'z'],
                route_name = data_points, 
                current_message = data_points, 
                advisory_id = data_points, 
                advisory_message = data_points, 
                detour_message = data_points,
                detour_id = data_points,
                detour_start_location = data_points, 
                detour_start_date_time = data_points,
                detour_end_date_time = data_points, 
                detour_reason = data_points,
                last_updated = data_points,
                isSnow = data_points))
        
        expected_df = create_data_frame(
                            route_name = [],
                            advisory_message = [],
                            detour_message = [],
                            detour_start_location = [],
                            detour_start_date_time = [],
                            detour_end_date_time = [],
                            detour_reason = [])

        pd.testing.assert_frame_equal(test_df, expected_df, check_dtype=False)

    def test_6_columns_are_dropped(self):
        test_df = scraper.filter_rows_and_columns(
            create_data_frame(
                route_id = ['b'],
                route_name = ['1'],
                current_message = ['test'],
                advisory_id = ['test'], 
                advisory_message = ['test'],
                detour_message = [None],
                detour_id = ['test'],
                detour_start_location = ['test'], 
                detour_start_date_time = ['test'],
                detour_end_date_time = ['test'], 
                detour_reason = ['test'],
                last_updated = ['test'],
                isSnow = ['test']))

        expected_df = create_data_frame(
                            route_name = ['1'],
                            advisory_message = ['test'],
                            detour_message = [None],
                            detour_start_location = ['test'],
                            detour_start_date_time = ['test'],
                            detour_end_date_time = ['test'],
                            detour_reason = ['test'])

        pd.testing.assert_frame_equal(test_df, expected_df, check_dtype=False)

class TestSeparateAdvisoriesAttachedToDetoursIntoNewDf():
    def test_detour_message_is_string_and_advisory_message_is_string_returns_row_where_only_advisory_message_and_route_name_are_populated(self):
        test_df = scraper.separate_advisories_attached_to_detours_into_new_df(
            create_data_frame(
                detour_message = ['string'],
                advisory_message = ['string'],
                route_name = ['4'], detour_start_location = ['test'], 
                detour_start_date_time = ['2022-04-19 08:13:00'], 
                detour_end_date_time = ['2022-04-19 08:13:00'], 
                detour_reason = ['test']))

        expected_df = create_data_frame(
                            detour_message = [None], 
                            advisory_message = ['string'], 
                            route_name = ['4'],
                            detour_start_location = [None], 
                            detour_start_date_time = [None],
                            detour_end_date_time = [None], 
                            detour_reason = [None])

        pd.testing.assert_frame_equal(test_df, expected_df)

    def test_route_name_is_duplicate_and_advisory_message_is_duplicate_returns_row_with_only_route_name_and_advisory_message_populated(self):
        test_df = scraper.separate_advisories_attached_to_detours_into_new_df(
            create_data_frame(
                detour_message = ['string', 'string2'],
                advisory_message = ['string', 'string'],
                route_name = ['4', '4'],
                detour_start_location = ['test', 'test2'], 
                detour_start_date_time = ['2022-04-19 08:13:00', '2022-12-31 23:59:00'], 
                detour_end_date_time = ['2022-04-19 08:13:00', '2022-12-31 23:59:00'], 
                detour_reason = ['test', 'test2']))

        expected_df = create_data_frame(
                            detour_message = [None],
                            advisory_message = ['string'], 
                            route_name = ['4'],
                            detour_start_location = [None], 
                            detour_start_date_time = [None],
                            detour_end_date_time = [None], 
                            detour_reason = [None])

        pd.testing.assert_frame_equal(test_df, expected_df)

class TestSplitAdvisoriesIntoNewDf():
    def test_advisory_message_not_null_and_detour_meesage_is_null_returns_row_with_only_route_name_and_advisory_message_populated(self):
        test_df = scraper.split_advisories_into_new_df(
            create_data_frame(
                detour_message = [None, 'string'],
                advisory_message = ['string', 'string2'], 
                route_name = ['4', '6'],
                detour_start_location = ['string', None], 
                detour_start_date_time = ['2022-04-19 08:13:00', None], 
                detour_end_date_time = ['2022-12-31 23:59:00', None], 
                detour_reason = ['string', None]))

        expected_df = create_data_frame(
                            detour_message = [None],
                            advisory_message = ['string'], 
                            route_name = ['4'],
                            detour_start_location = [None], 
                            detour_start_date_time = [None],
                            detour_end_date_time = [None], 
                            detour_reason = [None])

        pd.testing.assert_frame_equal(test_df, expected_df)

class TestConcatSeparatedAdvisoriesDfAndSplitAdvisoriesDf():
    def test_two_dataframes_returns_one_concated_dataframe(self):
        test_df = scraper.concat_separated_advisories_df_and_split_advisories_df(
            create_data_frame(
                detour_message = [None],
                advisory_message = ['string'], 
                route_name = ['4'],
                detour_start_location = [None], 
                detour_start_date_time = [None],
                detour_end_date_time = [None],
                detour_reason = [None]),
            create_data_frame(
                detour_message = [None],
                advisory_message = ['advisory'], 
                route_name = ['6'],
                detour_start_location = [None], 
                detour_start_date_time = [None],
                detour_end_date_time = [None], 
                detour_reason = [None]))

        expected_df = create_data_frame(
                            detour_message = [None, None], 
                            advisory_message = ['string', 'advisory'], 
                            route_name = ['4', '6'],
                            detour_start_location = [None, None], 
                            detour_start_date_time = [None, None],
                            detour_end_date_time = [None, None], 
                            detour_reason = [None, None])

        pd.testing.assert_frame_equal(test_df, expected_df)

class TestCleanConcatedAdvisoriesDf():
    def test_parsed_html_returns_final_advsiories_df(self):
        test_df = scraper.clean_concated_advisories_df(
            create_data_frame(
                detour_message = [None], 
                advisory_message = 
                    ['<h3 class=\"separated\">Stop Temporarily Discontinued - Broad and Arch Streets'\
                     ' (Northbound)</h3><p class=\"desc separated\">Until Further Notice</p><p>Due to '\
                     'construction, the northbound transit stop at Broad and Arch Streets has been '\
                     'temporarily discontinued.</p><h3 class=\"separated\">Stop Temporarily Discontinued - '\
                     'Northbound Service at Broad & Clearfield Sts.</h3><p class=\"desc separated\">Until Further '\
                     'Notice</p><p>Effective until further notice, the Northbound Transit Stop located at Broad &amp;'\
                     ' Clearfield Sts. has been discontinued.</p><p>Customers should use <a title=\"https://www.google.'\
                     'com/maps/place/W+Clearfield+St+%26+N+Broad+St,+Philadelphia,+PA+19132/@39.9998998,-75.1543064,18z/'\
                     'data=!4m5!3m4!1s0x89c6b7ff982f850d:0x5650a9c418e717a5!8m2!3d39.9999964!4d-75.1532174\" href=\"'\
                     'https://www.google.com/maps/place/W+Clearfield+St+%26+N+Broad+St,+Philadelphia,+PA+19132/@39.9998998,'\
                     '-75.1543064,18z/data=!4m5!3m4!1s0x89c6b7ff982f850d:0x5650a9c418e717a5!8m2!3d39.9999964!4d-75.1532174\"'\
                     'target=\"_blank\">Google Transit</a> to find alternate service options for Bus Routes 4 and 16 .</p>'], 
                route_name = ['4'],
                detour_start_location = [None], 
                detour_start_date_time = [None], detour_end_date_time = [None], 
                detour_reason = [None]))

        expected_df = pd.DataFrame({'Line': ['4', '4'], 'Title': ['Stop Temporarily Discontinued - Broad and Arch Streets (Northbound)', 
                                    'Stop Temporarily Discontinued - Northbound Service at Broad & Clearfield Sts.'],
                                    'Description': ['Due to construction, the northbound transit stop at Broad and Arch Streets has been temporarily discontinued.', 
                                    'Effective until further notice, the Northbound Transit Stop located at Broad & Clearfield Sts. has been discontinued. Customers '\
                                    'should use Google Transit to find alternate service options for Bus Routes 4 and 16 .'],
                                    'Detour Reason': [None, None], 'Type': ['Advisory', 'Advisory'],
                                    'Start Date': [None, None], 'End Date': ['Until Further Notice', 'Until Further Notice']})

        pd.testing.assert_frame_equal(test_df, expected_df)

class TestSeparateDetoursIntoNewDf():
    def test_detour_end_date_time_less_than_or_equal_to_3_days_in_future_returns_no_row_and_advisory_column_is_dropped(self):
        test_df = scraper.separate_detours_into_new_df(
            create_data_frame(
                route_name = ['1', '2'],
                advisory_message = ['test', 'test'],
                detour_message = ['test', 'test'],
                detour_start_location = ['test', 'test'], 
                detour_start_date_time = ['2022-04-19 08:13:00', '2022-12-31 23:59:00'],
                detour_end_date_time = ['2022-10-28 08:13:00', '2022-12-31 23:59:00'], 
                detour_reason = ['test', 'test']))
                                                                                      
        expected_df = create_data_frame(
                            route_name = ['2'],
                            detour_message = ['test'],
                            detour_start_location = ['test'],
                            detour_start_date_time = ['2022-12-31 23:59:00'],
                            detour_end_date_time = ['2022-12-31 23:59:00'],
                            detour_reason = ['test'])

        pd.testing.assert_frame_equal(test_df, expected_df)

# these next 2 tests actually return strings ??? needs updating
class TestCreateTitleColumn():
    def test_detour_start_location_with_double_spaces_or_space_Sts_returns_title_series_with_one_space_and_detour(self):
        test_series = create_data_frame(
            route_name = ['2'],
            detour_message = ['test'],
            detour_start_location = ['12th  & Walnut Sts.'],
            detour_start_date_time = ['2022-12-31 23:59:00'],
            detour_end_date_time = ['2022-12-31 23:59:00'],
            detour_reason = ['test']).apply(scraper.create_title_column, axis=1).copy(deep=True)
                                                                                      
        expected_series = pd.Series(['12th & Walnut, Detour'])

        pd.testing.assert_series_equal(test_series, expected_series)

class TestCreateDescriptionColumn():
    def test_regex_subs_return_amended_detour_message(self):
        test_series = create_data_frame(
            route_name = ['2'],
            detour_message = ['Until 4pm 10-27-2022, NB via 22nd, Left on Fairmount, Right on Pennsylvania, Right on 29th, Reg Rt'],
            detour_start_location = ['12th  & Walnut Sts.'], 
            detour_start_date_time = ['2022-12-31 23:59:00'],
            detour_end_date_time = ['2022-12-31 23:59:00'],
            detour_reason = ['test']).apply(scraper.create_description_column, axis=1).copy(deep=True)
                                                                                      
        expected_series = pd.Series(['Until 4pm 10-27-2022 NB via 22nd, L - Fairmount, R - Pennsylvania, R - 29th, Reg Rte'])

        pd.testing.assert_series_equal(test_series, expected_series)