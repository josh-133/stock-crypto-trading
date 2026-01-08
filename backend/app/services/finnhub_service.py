"""
Finnhub service for real-time stock price data via WebSocket.

Free tier limits:
- 60 API calls per minute
- WebSocket: 50 symbols max
- Real-time data with slight delay
"""
import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Optional, Callable
import websockets

logger = logging.getLogger(__name__)

# Get API key from environment
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
FINNHUB_WS_URL = "wss://ws.finnhub.io"
MAX_WEBSOCKET_SYMBOLS = 50


class FinnhubService:
    """Service for real-time stock prices via Finnhub WebSocket."""

    def __init__(self):
        self._api_key = FINNHUB_API_KEY
        self._websocket: Optional[websockets.WebSocketClientProtocol] = None
        self._subscribed_symbols: set[str] = set()
        self._latest_prices: dict[str, dict] = {}
        self._running = False
        self._callbacks: list[Callable] = []
        self._reconnect_delay = 5  # seconds

    @property
    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return bool(self._api_key)

    @property
    def subscribed_symbols(self) -> list[str]:
        """Get list of subscribed symbols."""
        return sorted(self._subscribed_symbols)

    def get_latest_price(self, symbol: str) -> Optional[dict]:
        """Get the latest cached price for a symbol."""
        return self._latest_prices.get(symbol.upper())

    def get_all_prices(self) -> dict[str, dict]:
        """Get all cached prices."""
        return self._latest_prices.copy()

    def add_callback(self, callback: Callable):
        """Add a callback to be called when prices update."""
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable):
        """Remove a callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    async def connect(self):
        """Connect to Finnhub WebSocket."""
        if not self.is_configured:
            logger.warning("Finnhub API key not configured. Set FINNHUB_API_KEY environment variable.")
            return

        self._running = True
        while self._running:
            try:
                url = f"{FINNHUB_WS_URL}?token={self._api_key}"
                async with websockets.connect(url) as websocket:
                    self._websocket = websocket
                    logger.info("Connected to Finnhub WebSocket")

                    # Resubscribe to previously subscribed symbols
                    for symbol in list(self._subscribed_symbols):
                        await self._send_subscribe(symbol)

                    # Listen for messages
                    async for message in websocket:
                        await self._handle_message(message)

            except websockets.exceptions.ConnectionClosed:
                logger.warning("Finnhub WebSocket connection closed")
            except Exception as e:
                logger.error(f"Finnhub WebSocket error: {e}")

            self._websocket = None
            if self._running:
                logger.info(f"Reconnecting in {self._reconnect_delay} seconds...")
                await asyncio.sleep(self._reconnect_delay)

    async def disconnect(self):
        """Disconnect from WebSocket."""
        self._running = False
        if self._websocket:
            await self._websocket.close()
            self._websocket = None

    async def subscribe(self, symbol: str) -> bool:
        """Subscribe to real-time updates for a symbol."""
        symbol = symbol.upper()

        if len(self._subscribed_symbols) >= MAX_WEBSOCKET_SYMBOLS:
            logger.warning(f"Cannot subscribe to {symbol}: max {MAX_WEBSOCKET_SYMBOLS} symbols reached")
            return False

        if symbol in self._subscribed_symbols:
            return True

        self._subscribed_symbols.add(symbol)

        if self._websocket:
            await self._send_subscribe(symbol)

        return True

    async def unsubscribe(self, symbol: str):
        """Unsubscribe from a symbol."""
        symbol = symbol.upper()

        if symbol not in self._subscribed_symbols:
            return

        self._subscribed_symbols.discard(symbol)
        self._latest_prices.pop(symbol, None)

        if self._websocket:
            await self._send_unsubscribe(symbol)

    async def _send_subscribe(self, symbol: str):
        """Send subscribe message to WebSocket."""
        if self._websocket:
            message = json.dumps({"type": "subscribe", "symbol": symbol})
            await self._websocket.send(message)
            logger.debug(f"Subscribed to {symbol}")

    async def _send_unsubscribe(self, symbol: str):
        """Send unsubscribe message to WebSocket."""
        if self._websocket:
            message = json.dumps({"type": "unsubscribe", "symbol": symbol})
            await self._websocket.send(message)
            logger.debug(f"Unsubscribed from {symbol}")

    async def _handle_message(self, message: str):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)

            if data.get("type") == "trade":
                trades = data.get("data", [])
                for trade in trades:
                    symbol = trade.get("s")
                    price = trade.get("p")
                    volume = trade.get("v")
                    timestamp = trade.get("t")

                    if symbol and price:
                        self._update_price(symbol, price, volume, timestamp)

            elif data.get("type") == "ping":
                # Respond to ping to keep connection alive
                pass

        except json.JSONDecodeError:
            logger.error(f"Failed to parse message: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    def _update_price(self, symbol: str, price: float, volume: int, timestamp: int):
        """Update the cached price for a symbol."""
        previous = self._latest_prices.get(symbol, {})
        previous_price = previous.get("price", price)

        change = price - previous_price
        change_percent = (change / previous_price * 100) if previous_price else 0

        self._latest_prices[symbol] = {
            "symbol": symbol,
            "price": price,
            "change": change,
            "change_percent": change_percent,
            "volume": volume,
            "timestamp": datetime.fromtimestamp(timestamp / 1000) if timestamp else datetime.now(),
            "source": "finnhub"
        }

        # Notify callbacks
        for callback in self._callbacks:
            try:
                callback(symbol, self._latest_prices[symbol])
            except Exception as e:
                logger.error(f"Callback error: {e}")


# Singleton instance
finnhub_service = FinnhubService()
