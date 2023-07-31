from opet.utils import http_get, to_json
from opet.exceptions import ProvinceNotFoundError

class OpetApiClient:
    def __init__(self):
        self.url = "https://api.opet.com.tr/api/fuelprices"

    def get_last_update(self):
        return http_get(f"{self.url}/lastupdate")

    def get_provinces(self):
        return http_get(f"{self.url}/provinces")

    def get_price(self, province_id: str):
        url = f"{self.url}/prices?ProvinceCode={province_id}&IncludeAllProducts=true"
        r = http_get(url)
        response = list(map(lambda x: dict(name=x["productName"], amount=x["amount"]), r[0]["prices"]))
        return response

    def price(self, province_id: str):
        _provinces = self.get_provinces()
        formatted_provinces = {str(item['code']): item['name'] for item in _provinces}
        province_name = formatted_provinces.get(f"{province_id}", None)
        if province_name is None:
            raise ProvinceNotFoundError(f"Sistemde {province_id} plaka koduna ait bir il bulunamadı.")

        result = dict(
            results=dict(
                province=province_name,
                lastUpdate=self.get_last_update()["lastUpdateDate"],
                prices=self.get_price(province_id)
            )
        )
        return to_json(result)


if __name__ == '__main__':
    client = OpetApiClient()
    print(client.get_provinces())
    print(client.get_price("28"))
    print(client.price("28"))
