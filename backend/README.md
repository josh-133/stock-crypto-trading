# Backend - FastAPI Trading Platform

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Strategy parameters
│   ├── api/
│   │   └── routes/          # API endpoints
│   ├── services/            # Business logic
│   ├── models/              # Pydantic models
│   └── core/                # Strategy logic
└── requirements.txt
```

## Key Endpoints

- `GET /api/stocks/{symbol}` - Stock data with SMAs
- `GET /api/signals` - Current trading signals
- `GET /api/portfolio` - Paper trading portfolio
- `POST /api/trades` - Execute trades
- `POST /api/backtest` - Run backtest
