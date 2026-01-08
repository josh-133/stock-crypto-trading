"""
API routes for managing the stock watchlist.
"""
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel

from ...services.watchlist_service import watchlist_service

MAX_SYMBOL_LENGTH = 10

router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])


class WatchlistResponse(BaseModel):
    symbols: list[str]
    count: int
    max_size: int


class SymbolActionResponse(BaseModel):
    success: bool
    message: str
    symbols: list[str]


class SearchResult(BaseModel):
    symbol: str
    name: str
    price: float | None
    in_watchlist: bool


@router.get("", response_model=WatchlistResponse)
async def get_watchlist():
    """Get the current watchlist."""
    symbols = watchlist_service.get_watchlist()
    return WatchlistResponse(
        symbols=symbols,
        count=len(symbols),
        max_size=50
    )


@router.post("/{symbol}", response_model=SymbolActionResponse)
async def add_to_watchlist(
    symbol: str = Path(..., min_length=1, max_length=MAX_SYMBOL_LENGTH)
):
    """Add a symbol to the watchlist."""
    result = watchlist_service.add_symbol(symbol)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return SymbolActionResponse(
        success=True,
        message=result["message"],
        symbols=watchlist_service.get_watchlist()
    )


@router.delete("/{symbol}", response_model=SymbolActionResponse)
async def remove_from_watchlist(
    symbol: str = Path(..., min_length=1, max_length=MAX_SYMBOL_LENGTH)
):
    """Remove a symbol from the watchlist."""
    result = watchlist_service.remove_symbol(symbol)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return SymbolActionResponse(
        success=True,
        message=result["message"],
        symbols=watchlist_service.get_watchlist()
    )


@router.get("/search", response_model=list[SearchResult])
async def search_symbols(
    q: str = Query(..., min_length=1, description="Search query for stock symbol")
):
    """Search for stock symbols."""
    results = watchlist_service.search_symbols(q)
    return [SearchResult(**r) for r in results]


@router.get("/validate/{symbol}")
async def validate_symbol(
    symbol: str = Path(..., min_length=1, max_length=MAX_SYMBOL_LENGTH)
):
    """Check if a symbol is valid."""
    is_valid = watchlist_service.validate_symbol(symbol)
    return {
        "symbol": symbol.upper(),
        "valid": is_valid,
        "in_watchlist": watchlist_service.is_in_watchlist(symbol)
    }
