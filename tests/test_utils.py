import pytest
from opet.utils import http_get, to_json
from opet.exceptions import Http200Error

# Headers that are expected to be used by http_get internally
EXPECTED_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/114.0.0.0 Safari/537.36'
    ),
    'Origin': 'https://www.opet.com.tr',
    'Host': 'api.opet.com.tr',
    'Channel': 'Web',
    'Accept-Language': 'tr-TR'
}


def test_http_get_success(mocker):
    """Test http_get for a successful request."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_requests_get = mocker.patch(
        'requests.get', return_value=mock_response
        )
    url = "http://testurl.com"
    data = http_get(url)

    mock_requests_get.assert_called_once_with(
        url,
        headers=EXPECTED_HEADERS,
        verify=True
    )
    assert data == {"key": "value"}


def test_http_get_failure(mocker):
    """Test http_get for a failed request."""
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch('requests.get', return_value=mock_response)

    url = "http://testurl.com"
    with pytest.raises(Http200Error):
        http_get(url)


def test_to_json():
    """Test the to_json function."""
    data = {"name": "test", "value": 123}
    expected_json = """{
  "name": "test",
  "value": 123
}"""
    assert to_json(data) == expected_json

    # Test with Turkish characters
    data_turkish = {"name": "İşlem", "value": "Ödeme"}
    expected_json_turkish = """{
  "name": "İşlem",
  "value": "Ödeme"
}"""
    assert to_json(data_turkish) == expected_json_turkish
