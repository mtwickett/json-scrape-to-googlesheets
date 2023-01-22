import pytest
from json_scrape.connections import get_disruptions_data

class TestGetDisruptionsData:
    def test_if_url_argument_is_an_empty_string(self):
        with pytest.raises(Exception) as exc_info:
            get_disruptions_data('')

        assert exc_info.type == Exception
        assert exc_info.value.args[0] == 'Provided URL is an empty string.'

    #def test_for_json_decoding_error(self):
    #    with pytest.raises(json.JSONDecodeError) as exc_info:
    #        get_disruptions_data('')

    #    assert exc_info.type == json.JSONDecodeError
    #    assert exc_info.value.args[0] == 'There\'s a problem decoding the json.'
