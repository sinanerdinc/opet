"""Utility functions for the Opet API client application.

This module provides helper functions for making HTTP requests and converting
data to JSON format, supporting the core operations of the Opet API client.
"""

import requests
from opet.exceptions import Http200Error
import json
from typing import Any, Dict, List, Union  # Added Union for to_json


def http_get(url: str) -> Any:
    """Makes a GET request to the specified URL and returns the JSON response.

    This function encapsulates the common settings for HTTP GET requests to the
    Opet API, including standard headers and error handling for non-200
    responses.

    Args:
        url: The URL to send the GET request to.

    Returns:
        The JSON response from the server, parsed into Python data structures.
        The exact structure depends on the API endpoint.

    Raises:
        Http200Error: If the HTTP status code of the response is not 200.
        requests.exceptions.RequestException: For network errors or other
                                              issues during the request.
    """
    headers: Dict[str, str] = {
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
    r: requests.Response = requests.get(url, headers=headers, verify=True)
    if r.status_code != 200:
        raise Http200Error(
            f"Request to '{url}' failed with status code {r.status_code}. "
            f"Response: {r.text}"
        )
    return r.json()


def to_json(data: Union[Dict[Any, Any], List[Any]]) -> str:
    """Converts a Python dictionary or list to a JSON string.

    This function formats the JSON string with an indent for readability and
    ensures that non-ASCII characters (like Turkish characters) are preserved.

    Args:
        data: The Python dictionary or list to be converted to JSON.

    Returns:
        A JSON string representation of the input data.
    """
    return json.dumps(data, ensure_ascii=False, indent=2)
