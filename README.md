# Portfolio Assessment Tool

A portfolio analytics tool built with **Domain-Driven Design (DDD)** architecture. It fetches portfolio data from Trading212 (or CSV) and generates AI-powered analysis reports.

## Architecture

This project follows Domain-Driven Design principles with clear layer separation:

```
PortfolioAssesment/
├── domain/                    # Domain Layer - Core business logic
│   ├── entities.py           # Portfolio, Position entities
│   ├── value_objects.py      # Money, Price, Quantity, Ticker, etc.
│   ├── repositories.py       # Repository interfaces (abstractions)
│   └── services.py           # Domain services (PortfolioAnalysisService)
│
├── application/               # Application Layer - Use cases
│   └── use_cases/
│       ├── fetch_portfolio.py
│       ├── analyze_portfolio.py
│       └── generate_report.py
│
├── infrastructure/            # Infrastructure Layer - External services
│   ├── repositories/         # Repository implementations
│   │   ├── trading212_repository.py
│   │   └── csv_repository.py
│   ├── services/            # External service clients
│   │   ├── trading212_client.py
│   │   ├── kraken_client.py
│   │   └── openai_llm_service.py
│   └── dependency_injection.py
│
└── presentation/             # Presentation Layer - User interface
    └── cli.py               # CLI entry point
```

## Features

- **Portfolio Analysis**: Computes total value, cost basis, and unrealized PnL
- **Diversification Metrics**: Breaks down portfolio by asset class and sector
- **Top Positions**: Highlights top positions by market value
- **AI-Powered Reports**: Generates insights using OpenAI (GPT models)
- **Multiple Data Sources**: Supports Trading212 API or CSV imports

## Requirements

- Python 3.8+ (tested with 3.11+)
- See `requirements.txt` for dependencies

## Environment Variables

### Trading212 API (optional)
- `TRADING212_BASE_URL` - Trading212 API base URL
- `TRADING212_STORAGE_ACCESS_KEY` - Trading212 storage access key
- `TRADING212_SECRET_STORAGE_ACCESS_KEY` - Trading212 secret storage access key
- `TRADING212_API_KEY` - Trading212 API key (alternative auth method)
- `MOCK_TRADING212=true` - Use mock data for testing

### OpenAI API (required for LLM reports)
- `OPENAI_API_KEY` - OpenAI API key

### Portfolio Configuration
- `PORTFOLIO_ID` - Portfolio identifier (default: "default")
- `PORTFOLIO_CSV_PATH` - Path to CSV file (alternative to API)

## Usage

### Basic Usage

```bash
python main.py
```

The tool will:
1. Fetch portfolio data (from API or CSV based on environment)
2. Analyze portfolio metrics
3. Generate an AI-powered report using OpenAI
4. Print the report to stdout

### CSV Mode

```bash
export PORTFOLIO_CSV_PATH=path/to/portfolio.csv
python main.py
```

### API Mode

```bash
export TRADING212_BASE_URL=https://api.trading212.example
export TRADING212_STORAGE_ACCESS_KEY=your_key
export TRADING212_SECRET_STORAGE_ACCESS_KEY=your_secret
export OPENAI_API_KEY=your_openai_key
python main.py
```

## Domain Model

### Entities
- **Portfolio**: Aggregate root representing a collection of positions
- **Position**: Individual holding with ticker, quantity, prices, and classifications

### Value Objects
- **Money**: Monetary amounts with currency
- **Price**: Price per unit
- **Quantity**: Number of shares/units
- **Ticker**: Stock ticker symbol
- **AssetClass**: Asset classification
- **Sector**: Sector classification

## Security Note

- Do not share your API keys publicly
- Store keys in environment variables or `.env` file (using `python-dotenv`)
- If keys are exposed, rotate them immediately in your accounts

## Development

### Adding a New Data Source

1. Create a new repository implementation in `infrastructure/repositories/`
2. Implement the `PortfolioRepository` interface
3. Create an API client in `infrastructure/services/` if needed
4. Update `dependency_injection.py` to wire it up

### Adding a New Use Case

1. Create a new use case class in `application/use_cases/`
2. Depend on domain entities and repository interfaces
3. Wire it up in the presentation layer

## Notes

- The domain layer has no dependencies on infrastructure
- All business logic lives in the domain layer
- External services are abstracted through interfaces
- Use cases coordinate domain logic and infrastructure
