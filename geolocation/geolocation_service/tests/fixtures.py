import unittest


def request_get_mock():
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "ip": "93.184.215.14",
        "type": "ipv4",
        "continent_code": "NA",
        "continent_name": "North America",
        "country_code": "US",
        "country_name": "United States",
        "region_code": "CA",
        "latitude": 40.7589111328125,
        "longitude": -73.97901916503906,
        "city": "Manhattan",
        "zip": "10020",
        "location": {
            "geoname_id": 5368361,
            "capital": "Washington D.C.",
            "languages": [{"code": "en", "name": "English", "native": "English"}],
            "country_flag": "https://assets.ipstack.com/flags/us.svg",
            "country_flag_emoji": "\ud83c\uddfa\ud83c\uddf8",
            "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
            "calling_code": "1",
            "is_eu": False,
        },
    }
    return mock_response


def request_get_mock_missing_fields():
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "ip": "93.184.215.14",
        "type": "ipv4",
        "continent_code": "NA",
        "continent_name": "North America",
        "country_code": "US",
        "country_name": "United States",
        "region_code": "CA",
        "latitude": None,
        "longitude": None,
        "city": "Manhattan",
        "zip": "10020",
        "location": {
            "geoname_id": 5368361,
            "capital": "Washington D.C.",
            "languages": [{"code": "en", "name": "English", "native": "English"}],
            "country_flag": "https://assets.ipstack.com/flags/us.svg",
            "country_flag_emoji": "\ud83c\uddfa\ud83c\uddf8",
            "country_flag_emoji_unicode": "U+1F1FA U+1F1F8",
            "calling_code": "1",
            "is_eu": False,
        },
    }
    return mock_response


def request_get_mock_success_false():
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": False,
        "error": {
            "code": 101,
            "info": "You have not supplied a valid API Access Key.",
            "type": "invalid_access_key",
        },
    }
    return mock_response


def request_get_mock_not_found():
    mock_response = unittest.mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": False,
        "error": {
            "code": 404,
            "info": "The requested resource does not exist.",
            "type": "404_not_found",
        },
    }
    return mock_response
