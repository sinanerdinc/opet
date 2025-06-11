"""Opet API Server uygulaması."""

from fastapi import FastAPI
from opet.server.controllers.fuel import FuelController


app = FastAPI(
    title="Opet Yakıt Fiyatları API",
    description="Opet yakıt fiyatlarına erişim sağlayan API",
    version="1.0.0"
)

# Kontrolcüleri oluştur
fuel_controller = FuelController()

# Route'ları ekle
app.include_router(fuel_controller.router)


@app.get("/")
async def root():
    """Ana sayfa."""
    return {"message": "Opet Yakıt Fiyatları API'sine Hoş Geldiniz"}
