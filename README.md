# Portfolio Assessment Tool

A simple portfolio analytics tool that fetches portfolio data from Trading212 (stocks/ETFs) or Kraken (crypto) and provides AI-powered analysis via interactive Q&A.

## Architecture

Simplified structure focused on clarity and maintainability:

```
PortfolioAssesment/
├── domain/
│   └── models.py          # Portfolio, Position, AssetClass, Sector
├── infrastructure/
│   ├── trading212_api.py  # Trading212 API client
│   ├── kraken_api.py      # Kraken API client
│   └── openai_client.py   # OpenRouter LLM client
└── main.py                # CLI entry point
```

## Features

- **Multi-Source Support**: Fetch portfolios from Trading212 (stocks/ETFs) or Kraken (crypto)
- **Portfolio Analysis**: Computes total value, cost basis, and P&L
- **AI-Powered Q&A**: Interactive chat with LLM about your portfolio
- **Real-Time Data**: Direct API integration with live portfolio data
- **Simple Architecture**: Clean, straightforward codebase

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `requests` - HTTP client
  - `openrouter` - OpenRouter API client
  - `python-dotenv` - Environment variable management
  - `python-trading212-alinalihassan` - Trading212 API client
  - `krakenex` - Kraken API client

## Environment Variables

Create a `.env` file in the project root:

```bash
# OpenRouter API (required for LLM)
OPENAI_API_KEY=sk-or-v1-your-openrouter-api-key-here
# Or use:
# OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here

# Trading212 API (required for --stock)
TRADING_212_ACCESS_KEY=your-trading212-api-key
TRADING_212_SECRET_STORAGE_ACCESS_KEY=your-trading212-secret-key
TRADING_212_BASE_URL=https://api.trading212.com  # Optional

# Kraken API (required for --crypto)
KRAKEN_API_KEY=your-kraken-api-key
KRAKEN_PRIVATE_KEY=your-kraken-private-key
```

## Usage

### Stocks/ETFs (Trading212)

```bash
python -m main --stock
```

Fetches your Trading212 portfolio and starts an interactive Q&A session.

### Crypto (Kraken)

```bash
python -m main --crypto
```

Fetches your Kraken crypto balances and starts an interactive Q&A session.

### Interactive Q&A

After loading your portfolio, you can ask questions like:
- "What's my total portfolio value?"
- "How is my portfolio diversified?"
- "What are my top positions?"
- "What's my risk exposure?"

Type `exit` to quit.

## Domain Model

### Portfolio
- Collection of positions
- Properties: `total_value`, `total_cost_basis`, `total_pnl`
- Methods: `get_positions_by_asset_class()`, `get_positions_by_sector()`, `get_top_positions()`

### Position
- Individual holding with:
  - `ticker`: Asset symbol (string)
  - `quantity`: Number of shares/units (float)
  - `avg_price`: Average purchase price (float)
  - `current_price`: Current market price (float)
  - `asset_class`: AssetClass enum (STOCK, ETF, CRYPTO, etc.)
  - `sector`: Sector enum (TECHNOLOGY, HEALTHCARE, etc.)
- Properties: `market_value`, `cost_basis`, `pnl`

### Enums
- **AssetClass**: STOCK, ETF, CRYPTO, BOND, COMMODITY, CASH, OTHER
- **Sector**: TECHNOLOGY, HEALTHCARE, FINANCIAL, CONSUMER, ENERGY, etc.

## Currency

All values are displayed in **USD**. The APIs return prices in USD, and the tool displays them as-is without conversion.

## Security

- **Never commit your `.env` file** - it contains sensitive API keys
- Store API keys in environment variables or `.env` file
- Rotate keys immediately if exposed
- Use read-only API keys when possible

## Development

### Adding a New Data Source

1. Create a new client class in `infrastructure/` (e.g., `binance_api.py`)
2. Implement a `get_portfolio()` method that returns a `Portfolio` object
3. Add command-line argument in `main.py`
4. Wire it up in the `main()` function

### Project Structure

- **domain/models.py**: Core data structures (Portfolio, Position, enums)
- **infrastructure/**: API clients for external services
- **main.py**: Entry point and CLI interface

## Notes

- The domain layer uses simple primitives (strings, floats) - no complex value objects
- All calculations are straightforward (price × quantity = value)
- API clients fetch raw data and convert to domain models
- LLM service uses OpenRouter for AI analysis
