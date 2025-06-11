"""Yakıt fiyatları için veri modelleri."""

from pydantic import BaseModel
from typing import List, Optional


class FuelPrice(BaseModel):
    """Yakıt fiyatı modeli."""
    name: str
    amount: float


class Province(BaseModel):
    """İl modeli."""
    code: str
    name: str


class PriceResponse(BaseModel):
    """Fiyat yanıt modeli."""
    province: str
    lastUpdate: str
    prices: List[FuelPrice]


class FuelPriceRequest(BaseModel):
    """Yakıt fiyatı istek modeli."""
    province_id: str
    fuel_type: Optional[str] = None


class LastUpdate(BaseModel):
    """Son güncelleme modeli."""
    lastUpdateDate: str
