"""Opet API'si için veri sağlayıcı."""

from opet.api import OpetApiClient
from opet.server.models.fuel import (
    Province,
    PriceResponse,
    LastUpdate
)
from typing import List
import json


class OpetProvider:
    """Opet API'si için veri sağlayıcı sınıfı."""

    def __init__(self):
        """API istemcisini başlatır."""
        self.client = OpetApiClient()

    def get_provinces(self) -> List[Province]:
        """Tüm illeri döner."""
        provinces = self.client.get_provinces()
        return [
            Province(
                code=str(province["code"]),
                name=province["name"]
            ) for province in provinces
        ]

    def get_prices(self, province_id: str) -> PriceResponse:
        """Belirli bir il için yakıt fiyatlarını döner."""
        result = self.client.price(province_id)
        parsed_result = json.loads(result)
        return PriceResponse(**parsed_result["results"])

    def get_last_update(self) -> LastUpdate:
        """Son güncelleme zamanını döner."""
        return LastUpdate(**self.client.get_last_update())
