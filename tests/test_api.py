import pytest
from unittest.mock import MagicMock, ANY
from opet.api import OpetApiClient
from opet.exceptions import ProvinceNotFoundError
from opet.utils import to_json

# Default province data to be returned by http_get during OpetApiClient.__init__
DEFAULT_PROVINCES_DATA = [{'code': 'DEFAULT', 'name': 'Default Province Test'}]

@pytest.fixture
def client_with_mock_http(mocker):
    """
    Fixture for OpetApiClient.
    Mocks 'opet.api.http_get' which is used by OpetApiClient.
    The mock is configured with default province data for the __init__ call.
    Returns the client instance and the mock for http_get.
    """
    # Patch http_get in the 'opet.api' module where it's imported and used.
    mock_http_get = mocker.patch('opet.api.http_get') 
    
    # Set a default return value for the provinces call made in OpetApiClient.__init__
    mock_http_get.return_value = DEFAULT_PROVINCES_DATA
    
    api_client = OpetApiClient() # __init__ will call the mocked opet.api.http_get
    
    return api_client, mock_http_get

def test_internal_province_loading(client_with_mock_http):
    """Test that provinces are loaded during __init__."""
    api_client, mock_http_get = client_with_mock_http
    # mock_http_get (opet.api.http_get) was called once during OpetApiClient.__init__
    assert mock_http_get.call_count == 1
    mock_http_get.assert_called_once_with(f"{api_client.url}/provinces")
    assert api_client._provinces_list == DEFAULT_PROVINCES_DATA
    assert api_client._provinces_map == {str(item['code']): item['name'] for item in DEFAULT_PROVINCES_DATA}

def test_get_last_update(client_with_mock_http, mocker):
    """Test get_last_update method."""
    api_client, mock_http_get = client_with_mock_http
    
    initial_call_count = mock_http_get.call_count # Should be 1 from __init__
    
    expected_data = {"lastUpdateDate": "2023-01-01T10:00:00"}
    mock_http_get.return_value = expected_data # For the get_last_update call
    
    data = api_client.get_last_update()
    
    assert mock_http_get.call_count == initial_call_count + 1
    # The last call is the one we are interested in
    mock_http_get.assert_called_with(f"{api_client.url}/lastupdate")
    assert data == expected_data

def test_get_provinces(client_with_mock_http, mocker):
    """Test get_provinces method."""
    api_client, mock_http_get = client_with_mock_http
    initial_call_count = mock_http_get.call_count # Should be 1 from __init__
        
    expected_data = [{"code": "34", "name": "Istanbul"}]
    mock_http_get.return_value = expected_data 
    
    data = api_client.get_provinces()
    
    assert mock_http_get.call_count == initial_call_count + 1
    mock_http_get.assert_called_with(f"{api_client.url}/provinces")
    assert data == expected_data
    # Check that the internal _provinces_list is from __init__, not this call.
    assert api_client._provinces_list == DEFAULT_PROVINCES_DATA

def test_get_price_success(client_with_mock_http, mocker):
    """Test get_price method for success."""
    api_client, mock_http_get = client_with_mock_http
    initial_call_count = mock_http_get.call_count # Should be 1 from __init__
    province_id = "34"
        
    raw_price_data_from_http = [{"prices": [{"productName": "Petrol", "amount": 20.0}]}]
    expected_processed_data = [{"name": "Petrol", "amount": 20.0}] 

    mock_http_get.return_value = raw_price_data_from_http
    
    processed_data = api_client.get_price(province_id)
    
    assert mock_http_get.call_count == initial_call_count + 1
    expected_url = f"{api_client.url}/prices?ProvinceCode={province_id}&IncludeAllProducts=true"
    mock_http_get.assert_called_with(expected_url)
    assert processed_data == expected_processed_data

def test_price_success(client_with_mock_http, mocker):
    """Test price method for successful retrieval and formatting."""
    api_client, mock_http_get = client_with_mock_http 
    
    # Verify the __init__ call first
    assert mock_http_get.call_count == 1
    mock_http_get.assert_called_with(f"{api_client.url}/provinces")

    province_id_to_test = "DEFAULT" # Matches DEFAULT_PROVINCES_DATA

    last_update_data = {'lastUpdateDate': '2023-01-01T10:00:00'}
    raw_prices_data_for_get_price = [{'prices': [{'productName': 'Petrol', 'amount': 20.0}]}]
    processed_prices_data = [{'name': 'Petrol', 'amount': 20.0}]

    # Configure side_effect for the two calls made *within* client.price():
    # get_last_update() and then get_price()
    mock_http_get.side_effect = [last_update_data, raw_prices_data_for_get_price]

    result_json_str = api_client.price(province_id_to_test)

    expected_output_structure = {
        "results": {
            "province": DEFAULT_PROVINCES_DATA[0]['name'], 
            "lastUpdate": last_update_data['lastUpdateDate'],
            "prices": processed_prices_data
        }
    }
    expected_json_output = to_json(expected_output_structure)
    assert result_json_str == expected_json_output
    
    # Assert http_get calls
    # Total 3 calls: 1 from __init__ (already asserted), 2 from price() method.
    assert mock_http_get.call_count == 1 + 2 
    
    calls = mock_http_get.call_args_list
    assert len(calls) == 3
    assert calls[0] == mocker.call(f"{api_client.url}/provinces") # From __init__
    assert calls[1] == mocker.call(f"{api_client.url}/lastupdate") # From price() -> get_last_update()
    assert calls[2] == mocker.call(f"{api_client.url}/prices?ProvinceCode={province_id_to_test}&IncludeAllProducts=true") # From price() -> get_price()


def test_price_province_not_found(client_with_mock_http, mocker):
    """Test price method when province ID is not found (using data loaded in __init__)."""
    api_client, mock_http_get = client_with_mock_http
    
    # Verify the __init__ call
    assert mock_http_get.call_count == 1
    mock_http_get.assert_called_with(f"{api_client.url}/provinces")
                                                    
    province_id_not_in_default = "NON_EXISTENT_ID"
    expected_error_message = f"Sistemde {province_id_not_in_default} plaka koduna ait bir il bulunamadı."

    # Store call count before the action that might (or might not) make new calls
    initial_call_count_after_init = mock_http_get.call_count 

    with pytest.raises(ProvinceNotFoundError, match=expected_error_message):
        api_client.price(province_id_not_in_default)
    
    # Ensure no *new* http_get calls were made by the price() method itself.
    assert mock_http_get.call_count == initial_call_count_after_init # Should still be 1
