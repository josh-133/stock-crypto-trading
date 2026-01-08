"""
FastAPI application entry point.

This is the main application that serves the trading platform API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import API_CONFIG
from .api.routes import stocks, signals, portfolio, trades, backtest, benchmark

# Create FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"],
)

# Configure CORS for frontend
# Security: Explicitly specify allowed methods and headers instead of wildcards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Only methods we actually use
    allow_headers=["Content-Type", "Authorization"],  # Only headers we need
)

# Include routers
app.include_router(stocks.router, prefix="/api")
app.include_router(signals.router, prefix="/api")
app.include_router(portfolio.router, prefix="/api")
app.include_router(trades.router, prefix="/api")
app.include_router(backtest.router, prefix="/api")
app.include_router(benchmark.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": API_CONFIG["title"],
        "version": API_CONFIG["version"],
        "description": API_CONFIG["description"],
        "docs": "/docs",
        "endpoints": {
            "stocks": "/api/stocks/{symbol}",
            "signals": "/api/signals",
            "portfolio": "/api/portfolio",
            "trades": "/api/trades",
            "backtest": "/api/backtest",
            "benchmark": "/api/benchmark",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
