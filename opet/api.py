"""Provides access to Opet Fuel Prices API through OpetApiClient."""

from opet.utils import http_get, to_json
from opet.exceptions import ProvinceNotFoundError
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class FuelPrice(TypedDict):
    """A fuel price record."""
    name: str
    amount: float


class Province(TypedDict):
    """A province record."""
    code: str
    name: str


class LastUpdateInfo(TypedDict):
    """Last update information."""
    lastUpdateDate: str


class FormattedPriceResult(TypedDict):
    """Price result structure."""
    province: str
    lastUpdate: str
    prices: List[FuelPrice]


class PriceResponse(TypedDict):
    """Main JSON response structure."""
    results: FormattedPriceResult


class OpetApiClient:
    """Opet Fuel Prices API client."""

    def __init__(self) -> None:
        """Loads the list of provinces."""
        self.url: str = "https://api.opet.com.tr/api/fuelprices"
        self._provinces_list: List[Province] = self.get_provinces()
        self._provinces_map: Dict[str, str] = {
            str(item['code']): item['name'] for item in self._provinces_list
        }

    def get_last_update(self) -> LastUpdateInfo:
        """Returns the last update time."""
        return http_get(f"{self.url}/lastupdate")

    def get_provinces(self) -> List[Province]:
        """Returns all provinces."""
        return http_get(f"{self.url}/provinces")

    def get_price(self, province_id: str) -> List[FuelPrice]:
        """Returns fuel prices for a province."""
        url: str = (
            f"{self.url}/prices?ProvinceCode={province_id}"
            "&IncludeAllProducts=true"
        )
        raw_response: List[Dict[str, Any]] = http_get(url)
        if not raw_response or "prices" not in raw_response[0]:
            return []
        response: List[FuelPrice] = [
            {"name": x["productName"], "amount": x["amount"]}
            for x in raw_response[0]["prices"]
        ]
        return response

    def _normalize_plate_code(self, plate_code: str) -> str:
        """Normalizes plate code by removing leading zeros if numeric."""
        if plate_code.isdigit():
            return str(int(plate_code))
        return plate_code

    def price(self, province_id: str) -> str:
        """Returns prices as JSON for a province."""
        normalized_id = self._normalize_plate_code(province_id)
        province_name: Optional[str] = self._provinces_map.get(normalized_id)
        if province_name is None:
            raise ProvinceNotFoundError(
                f"No province found with plate code {province_id} "
                "in the system."
            )
        last_update_info: LastUpdateInfo = self.get_last_update()
        fuel_prices: List[FuelPrice] = self.get_price(normalized_id)
        result: PriceResponse = {
            "results": {
                "province": province_name,
                "lastUpdate": last_update_info["lastUpdateDate"],
                "prices": fuel_prices
            }
        }
        return to_json(result)


if __name__ == '__main__':
    client = OpetApiClient()
    print("\nAvailable Provinces (first 5):")
    provinces = client.get_provinces()
    for p in provinces[:5]:
        print(f"- Code: {p['code']}, Name: {p['name']}")
    if client._provinces_list:
        print(f"\nClient has {len(client._provinces_list)} provinces loaded.")
        sample_code = client._provinces_list[0]['code']
        print(f"\nTesting with a valid province code: {sample_code}")
        print(f"\nPrices for province code {sample_code} (direct get_price):")
        prices_direct = client.get_price(sample_code)
        for price_info in prices_direct:
            print(f"- {price_info['name']}: {price_info['amount']}")
        print(
            f"\nFormatted price information for province code {sample_code}"
            " (using price method):"
        )
        formatted_prices = client.price(sample_code)
        print(formatted_prices)
        if "34" in client._provinces_map:
            print("\nFormatted price information for İstanbul (34):")
            print(client.price("34"))
        else:
            print("\nİstanbul (34) not found in loaded provinces.")
    else:
        print("\nNo provinces loaded at initialization.")
    print("\nLast Update Info:")
    print(client.get_last_update())
