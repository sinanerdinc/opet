from opet.utils import yesterday, http_get, to_json
from opet.exceptions import ProvinceNotFoundError

class OpetApiClient:
    def __init__(self):
        self.url = "https://api.opet.com.tr/api/fuelprices"

    def get_provinces(self):
        return http_get(f"{self.url}/provinces")

    def get_districts(self, province_id):
        return http_get(f"{self.url}/provinces/{province_id}/districts")

    def get_price(self, district_id: str):
        date = yesterday()
        url = f"{self.url}/prices/archive?DistrictCode={district_id}&StartDate={date}&EndDate={date}&IncludeAllProducts=true"
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
                prices=self.get_price(self.get_districts(province_id)[0]["code"])
            )
        )
        return to_json(result)


if __name__ == '__main__':
    client = OpetApiClient()
    print(client.price("28"))
