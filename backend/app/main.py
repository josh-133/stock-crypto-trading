"""
FastAPI application entry point.

This is the main application that serves the trading platform API.
"""
import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .config import API_CONFIG
from .api.routes import stocks, signals, portfolio, trades, backtest, benchmark, watchlist
from .services.finnhub_service import finnhub_service
from .services.watchlist_service import watchlist_service

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
app.include_router(watchlist.router)


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
            "watchlist": "/api/watchlist",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except ValueError:
            pass  # Already removed

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass


ws_manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    """Start Finnhub WebSocket connection on app startup."""
    if finnhub_service.is_configured:
        # Subscribe to all symbols in watchlist
        for symbol in watchlist_service.get_watchlist():
            await finnhub_service.subscribe(symbol)

        # Start WebSocket connection in background
        asyncio.create_task(finnhub_service.connect())

        # Add callback to broadcast price updates
        def on_price_update(symbol: str, price_data: dict):
            asyncio.create_task(ws_manager.broadcast({
                "type": "price_update",
                "data": price_data
            }))

        finnhub_service.add_callback(on_price_update)


@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from Finnhub on shutdown."""
    await finnhub_service.disconnect()


@app.websocket("/ws/prices")
async def websocket_prices(websocket: WebSocket):
    """WebSocket endpoint for real-time price updates."""
    await ws_manager.connect(websocket)

    try:
        # Send current prices on connect
        prices = finnhub_service.get_all_prices()
        if prices:
            await websocket.send_json({
                "type": "initial_prices",
                "data": prices
            })

        # Keep connection alive and handle client messages
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                # Handle subscribe/unsubscribe requests from client
                if message.get("action") == "subscribe":
                    symbol = message.get("symbol", "").upper()
                    if symbol:
                        await finnhub_service.subscribe(symbol)
                elif message.get("action") == "unsubscribe":
                    symbol = message.get("symbol", "").upper()
                    if symbol:
                        await finnhub_service.unsubscribe(symbol)
            except json.JSONDecodeError:
                pass

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@app.get("/api/realtime/status")
async def realtime_status():
    """Get real-time data connection status."""
    return {
        "configured": finnhub_service.is_configured,
        "subscribed_symbols": finnhub_service.subscribed_symbols,
        "symbol_count": len(finnhub_service.subscribed_symbols),
        "max_symbols": 50,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
