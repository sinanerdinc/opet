"""Opet API Server uygulaması."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
from opet.api import OpetApiClient, FuelPrice

app = FastAPI(
    title="Opet Yakıt Fiyatları API",
    description="Opet yakıt fiyatlarına erişim sağlayan API",
    version="1.0.0"
)

# API istemcisini oluştur
client = OpetApiClient()

class PriceResponse(BaseModel):
    """Fiyat yanıt modeli."""
    province: str
    lastUpdate: str
    prices: List[FuelPrice]

@app.get("/")
async def root():
    """Ana sayfa."""
    return {"message": "Opet Yakıt Fiyatları API'sine Hoş Geldiniz"}

@app.get("/provinces")
async def get_provinces():
    """Tüm illeri listeler."""
    return client.get_provinces()

@app.get("/prices/{province_id}", response_model=PriceResponse)
async def get_prices(province_id: str):
    """Belirli bir il için yakıt fiyatlarını döner."""
    try:
        result = client.price(province_id)
        # JSON string'ini parse et
        parsed_result = json.loads(result)
        return parsed_result["results"]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/last-update")
async def get_last_update():
    """Son güncelleme zamanını döner."""
    return client.get_last_update() 