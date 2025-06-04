"""API sunucusunu başlatır."""

import uvicorn
from opet.server.app import app

if __name__ == "__main__":
    uvicorn.run(
        "opet.server.app:app",
        host="0.0.0.0",
        port=5050,
        reload=True
    ) 