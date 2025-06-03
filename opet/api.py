"""Provides the OpetApiClient for interacting with the Opet Fuel Prices API.

This module contains the OpetApiClient class, which is responsible for fetching
fuel price information, province data, and last update times from the
official Opet API. It handles the construction of API requests and the
formatting of responses.
"""

from opet.utils import http_get, to_json
from opet.exceptions import ProvinceNotFoundError
from typing import List, Dict, Any, TypedDict, Optional # Added TypedDict and Optional

# Define TypedDicts for structured data if possible and known.
# This improves clarity for complex dictionary structures.

class FuelPrice(TypedDict):
    """Represents the structure of a single fuel price entry."""
    name: str
    amount: float # Assuming amount is a float, adjust if necessary

class Province(TypedDict):
    """Represents the structure of a province entry from the API."""
    code: str # Or int, if the API guarantees integer codes
    name: str

class LastUpdateInfo(TypedDict):
    """Represents the structure of the last update information from the API."""
    lastUpdateDate: str # Assuming ISO format string, e.g., "2023-01-01T10:00:00"

class FormattedPriceResult(TypedDict):
    """Represents the structure of the main results dictionary in the price method."""
    province: str
    lastUpdate: str
    prices: List[FuelPrice]

class PriceResponse(TypedDict):
    """Represents the overall structure of the JSON returned by the price method."""
    results: FormattedPriceResult


class OpetApiClient:
    """A client for interacting with the Opet Fuel Prices API.

    This client fetches province information upon initialization and uses this
    data to provide fuel prices for specified provinces, along with last update
    information.

    Attributes:
        url (str): The base URL for the Opet Fuel Prices API.
        _provinces_list (List[Province]): A list of province dictionaries fetched from the API.
        _provinces_map (Dict[str, str]): A mapping from province codes to province names.
    """
    def __init__(self) -> None:
        """Initializes the OpetApiClient.

        Fetches the list of provinces from the Opet API and stores it for later use.
        """
        self.url: str = "https://api.opet.com.tr/api/fuelprices"
        self._provinces_list: List[Province] = self.get_provinces()
        self._provinces_map: Dict[str, str] = {
            str(item['code']): item['name'] for item in self._provinces_list
        }

    def get_last_update(self) -> LastUpdateInfo:
        """Fetches the last update time for fuel prices.

        Returns:
            A dictionary containing the last update date string.
            Example: {"lastUpdateDate": "2023-10-27T14:30:00"}

        Raises:
            Http200Error: If the API request fails (e.g., non-200 status).
            requests.exceptions.RequestException: For network or request issues.
        """
        return http_get(f"{self.url}/lastupdate")

    def get_provinces(self) -> List[Province]:
        """Fetches the list of all provinces from the Opet API.

        This method is primarily used during client initialization but can be
        called directly if needed.

        Returns:
            A list of dictionaries, where each dictionary represents a province
            and contains 'code' and 'name'.
            Example: [{"code": "34", "name": "İstanbul"}, ...]

        Raises:
            Http200Error: If the API request fails.
            requests.exceptions.RequestException: For network or request issues.
        """
        return http_get(f"{self.url}/provinces")

    def get_price(self, province_id: str) -> List[FuelPrice]:
        """Fetches fuel prices for a specific province ID.

        Args:
            province_id: The plate code (plaka kodu) of the province as a string.

        Returns:
            A list of dictionaries, where each dictionary represents a fuel product
            and its price (e.g., {"name": "Kurşunsuz Benzin 95", "amount": 35.60}).
            Returns an empty list if the province is valid but has no price data,
            though the API structure suggests it would be `r[0]["prices"]`.

        Raises:
            Http200Error: If the API request fails.
            requests.exceptions.RequestException: For network or request issues.
            IndexError: If the API response for prices is not in the expected format
                        (e.g., empty list `r` or `r[0]` not having "prices").
        """
        url: str = f"{self.url}/prices?ProvinceCode={province_id}&IncludeAllProducts=true"
        # The http_get function is expected to return a list of dictionaries for this endpoint,
        # where the first dictionary contains the "prices" list.
        # Example raw response from http_get for this URL (based on previous tests):
        # [{"districtCode": null, "districtName": null, "prices": [...]}]
        raw_response: List[Dict[str, Any]] = http_get(url)
        
        if not raw_response or "prices" not in raw_response[0]:
            # Or handle more gracefully depending on expected API behavior for no prices
            return [] 
            
        # Map to FuelPrice structure
        response: List[FuelPrice] = [
            {"name": x["productName"], "amount": x["amount"]}
            for x in raw_response[0]["prices"]
        ]
        return response

    def price(self, province_id: str) -> str:
        """Fetches and formats fuel prices for a given province ID.

        This method uses the pre-loaded province data to find the province name
        and then fetches the latest fuel prices and last update time. The result
        is returned as a JSON string.

        Args:
            province_id: The plate code (plaka kodu) of the province as a string.

        Returns:
            A JSON string containing the province name, last update time, and
            a list of fuel prices.
            Example:
            ```json
            {
              "results": {
                "province": "İstanbul",
                "lastUpdate": "2023-10-27T15:00:00",
                "prices": [
                  {"name": "Kurşunsuz Benzin 95", "amount": 35.60},
                  {"name": "Motorin", "amount": 40.10}
                ]
              }
            }
            ```

        Raises:
            ProvinceNotFoundError: If the provided `province_id` is not found in
                                   the pre-loaded province map.
            Http200Error: If underlying API requests for last update or prices fail.
            requests.exceptions.RequestException: For network or request issues.
        """
        province_name: Optional[str] = self._provinces_map.get(str(province_id))
        if province_name is None:
            raise ProvinceNotFoundError(f"Sistemde {province_id} plaka koduna ait bir il bulunamadı.")

        last_update_info: LastUpdateInfo = self.get_last_update()
        fuel_prices: List[FuelPrice] = self.get_price(province_id)

        result: PriceResponse = { # Conforms to PriceResponse TypedDict
            "results": {
                "province": province_name,
                "lastUpdate": last_update_info["lastUpdateDate"],
                "prices": fuel_prices
            }
        }
        return to_json(result)


if __name__ == '__main__':
    # Basic usage example
    client = OpetApiClient()
    
    print("\nAvailable Provinces (first 5):")
    provinces = client.get_provinces() # Re-fetches if called directly
    for p in provinces[:5]:
        print(f"- Code: {p['code']}, Name: {p['name']}")

    # Using internal list (fetched at init)
    if client._provinces_list:
      print(f"\nClient has {len(client._provinces_list)} provinces loaded internally.")
      sample_province_code_to_test = client._provinces_list[0]['code'] # Get a valid code
      print(f"\nTesting with a valid province code: {sample_province_code_to_test}")


      print(f"\nPrices for province code {sample_province_code_to_test} (direct get_price):")
      prices_direct = client.get_price(sample_province_code_to_test)
      for price_info in prices_direct:
          print(f"- {price_info['name']}: {price_info['amount']}")
      
      print(f"\nFormatted price information for province code {sample_province_code_to_test} (using price method):")
      formatted_prices = client.price(sample_province_code_to_test)
      print(formatted_prices)

      # Test with a common province like Istanbul '34' if available
      if "34" in client._provinces_map:
          print("\nFormatted price information for İstanbul (34):")
          print(client.price("34"))
      else:
          print("\nİstanbul (34) not found in loaded provinces for specific test.")

    else:
        print("\nNo provinces loaded at initialization, cannot run detailed examples.")

    print("\nLast Update Info:")
    print(client.get_last_update())
