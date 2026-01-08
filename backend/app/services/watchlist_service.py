"""
Watchlist service for managing user's stock watchlist.
Stores watchlist in memory with JSON file persistence.
"""
import json
import logging
from pathlib import Path
from typing import Optional
import yfinance as yf

logger = logging.getLogger(__name__)

# Default watchlist for new users
DEFAULT_WATCHLIST = ["AAPL", "MSFT", "GOOGL", "SPY"]
MAX_WATCHLIST_SIZE = 50
WATCHLIST_FILE = Path(__file__).parent.parent.parent / "data" / "watchlist.json"


class WatchlistService:
    """Service for managing the user's stock watchlist."""

    def __init__(self):
        self._watchlist: set[str] = set()
        self._load_watchlist()

    def _load_watchlist(self):
        """Load watchlist from file or use defaults."""
        try:
            if WATCHLIST_FILE.exists():
                with open(WATCHLIST_FILE, "r") as f:
                    data = json.load(f)
                    self._watchlist = set(data.get("symbols", DEFAULT_WATCHLIST))
                    logger.info(f"Loaded watchlist with {len(self._watchlist)} symbols")
            else:
                self._watchlist = set(DEFAULT_WATCHLIST)
                self._save_watchlist()
                logger.info("Created default watchlist")
        except Exception as e:
            logger.error(f"Error loading watchlist: {e}")
            self._watchlist = set(DEFAULT_WATCHLIST)

    def _save_watchlist(self):
        """Save watchlist to file."""
        try:
            WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(WATCHLIST_FILE, "w") as f:
                json.dump({"symbols": sorted(self._watchlist)}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving watchlist: {e}")

    def get_watchlist(self) -> list[str]:
        """Get all symbols in the watchlist."""
        return sorted(self._watchlist)

    def add_symbol(self, symbol: str) -> dict:
        """
        Add a symbol to the watchlist.
        Returns dict with success status and message.
        """
        symbol = symbol.upper().strip()

        if len(self._watchlist) >= MAX_WATCHLIST_SIZE:
            return {
                "success": False,
                "message": f"Watchlist full. Maximum {MAX_WATCHLIST_SIZE} symbols allowed."
            }

        if symbol in self._watchlist:
            return {
                "success": False,
                "message": f"{symbol} is already in your watchlist."
            }

        # Validate symbol exists
        if not self.validate_symbol(symbol):
            return {
                "success": False,
                "message": f"{symbol} is not a valid stock symbol."
            }

        self._watchlist.add(symbol)
        self._save_watchlist()

        return {
            "success": True,
            "message": f"{symbol} added to watchlist."
        }

    def remove_symbol(self, symbol: str) -> dict:
        """
        Remove a symbol from the watchlist.
        Returns dict with success status and message.
        """
        symbol = symbol.upper().strip()

        if symbol not in self._watchlist:
            return {
                "success": False,
                "message": f"{symbol} is not in your watchlist."
            }

        self._watchlist.discard(symbol)
        self._save_watchlist()

        return {
            "success": True,
            "message": f"{symbol} removed from watchlist."
        }

    def validate_symbol(self, symbol: str) -> bool:
        """Check if a symbol is valid and tradeable."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            # Check if we got valid data (market cap or price exists)
            return info.get("regularMarketPrice") is not None or info.get("marketCap") is not None
        except Exception:
            return False

    def search_symbols(self, query: str, limit: int = 10) -> list[dict]:
        """
        Search for stock symbols matching a query.
        Returns list of matching symbols with basic info.
        """
        query = query.upper().strip()
        if len(query) < 1:
            return []

        results = []

        # First, check if exact symbol exists
        try:
            ticker = yf.Ticker(query)
            info = ticker.info
            if info.get("regularMarketPrice") is not None:
                results.append({
                    "symbol": query,
                    "name": info.get("shortName", info.get("longName", query)),
                    "price": info.get("regularMarketPrice"),
                    "in_watchlist": query in self._watchlist
                })
        except Exception:
            pass

        return results[:limit]

    def is_in_watchlist(self, symbol: str) -> bool:
        """Check if a symbol is in the watchlist."""
        return symbol.upper().strip() in self._watchlist


# Singleton instance
watchlist_service = WatchlistService()
