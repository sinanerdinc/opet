"""Starts the API server."""

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "opet.server.app:app",
        host="0.0.0.0",
        reload=True
    )
