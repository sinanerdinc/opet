"""Yakıt fiyatları için kontrolcü."""

from fastapi import APIRouter, HTTPException
from opet.server.models.fuel import (
    Province,
    PriceResponse,
    LastUpdate
)
from opet.server.providers.opet import OpetProvider
from typing import List


class FuelController:
    """Yakıt fiyatları için kontrolcü sınıfı."""

    def __init__(self):
        """Kontrolcüyü başlatır."""
        self.provider = OpetProvider()
        self.router = APIRouter(prefix="/fuel", tags=["fuel"])

        # Route'ları tanımla
        self.router.add_api_route(
            "/provinces",
            self.get_provinces,
            response_model=List[Province],
            methods=["GET"]
        )
        self.router.add_api_route(
            "/prices/{province_id}",
            self.get_prices,
            response_model=PriceResponse,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/last-update",
            self.get_last_update,
            response_model=LastUpdate,
            methods=["GET"]
        )

    async def get_provinces(self) -> List[Province]:
        """Tüm illeri listeler."""
        return self.provider.get_provinces()

    async def get_prices(self, province_id: str) -> PriceResponse:
        """Belirli bir il için yakıt fiyatlarını döner."""
        try:
            return self.provider.get_prices(province_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def get_last_update(self) -> LastUpdate:
        """Son güncelleme zamanını döner."""
        return self.provider.get_last_update()
