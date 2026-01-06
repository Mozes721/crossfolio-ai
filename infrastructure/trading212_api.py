import os
from trading212 import Trading212 as T212Client
from trading212.models import Position as T212Position
from domain.repositories import PortfolioRepository
from domain.entities import Portfolio, Position
from domain.value_objects import Ticker, Quantity, Price, AssetClass, Sector


class Trading212Client(PortfolioRepository):
    def __init__(self, base_url: str, access_key: str, secret_key: str):
        self.use_mock = os.environ.get("MOCK_TRADING212", "false").lower() == "true"
        
        if not self.use_mock:
            if not access_key:
                raise ValueError("Trading212 API key is required in non-mock mode")
            
            host = "live.trading212.com"
            if base_url and "demo" in base_url.lower():
                host = "demo.trading212.com"
            
            self.client = T212Client(api_key=access_key, host=host)
        else:
            self.client = None

    def get_portfolio(self) -> Portfolio:
        if self.use_mock:
            return self._get_mock_portfolio()
        
        try:
            t212_positions = self.client.fetch_all_open_positions()
            return self._convert_to_domain_portfolio(t212_positions)
        except Exception as e:
            raise ConnectionError(f"Failed to fetch portfolio from Trading212: {e}")

    def _convert_to_domain_portfolio(self, t212_positions: list) -> Portfolio:
        positions = []
        
        for t212_pos in t212_positions:
            position = Position(
                ticker=Ticker(symbol=t212_pos.ticker),
                quantity=Quantity(value=int(t212_pos.quantity)),
                avg_price=Price(value=t212_pos.averagePrice),
                current_price=Price(value=t212_pos.currentPrice),
                asset_class=AssetClass.OTHER,
                sector=Sector.OTHER
            )
            positions.append(position)
        
        return Portfolio(positions=positions)

    def _get_mock_portfolio(self) -> Portfolio:
        mock_positions = [
            Position(
                ticker=Ticker(symbol="AAPL"),
                quantity=Quantity(value=10),
                avg_price=Price(value=150.0),
                current_price=Price(value=195.0),
                asset_class=AssetClass.STOCK,
                sector=Sector.TECHNOLOGY
            ),
            Position(
                ticker=Ticker(symbol="MSFT"),
                quantity=Quantity(value=5),
                avg_price=Price(value=250.0),
                current_price=Price(value=380.0),
                asset_class=AssetClass.STOCK,
                sector=Sector.TECHNOLOGY
            ),
            Position(
                ticker=Ticker(symbol="JNJ"),
                quantity=Quantity(value=20),
                avg_price=Price(value=160.0),
                current_price=Price(value=155.0),
                asset_class=AssetClass.STOCK,
                sector=Sector.HEALTHCARE
            ),
            Position(
                ticker=Ticker(symbol="VOO"),
                quantity=Quantity(value=15),
                avg_price=Price(value=400.0),
                current_price=Price(value=450.0),
                asset_class=AssetClass.ETF,
                sector=Sector.OTHER
            ),
            Position(
                ticker=Ticker(symbol="BTC"),
                quantity=Quantity(value=2),
                avg_price=Price(value=30000.0),
                current_price=Price(value=43000.0),
                asset_class=AssetClass.CRYPTO,
                sector=Sector.OTHER
            ),
        ]
        return Portfolio(positions=mock_positions)

    def _map_asset_class(self, asset_class: str) -> AssetClass:
        mapping = {
            "stock": AssetClass.STOCK,
            "etf": AssetClass.ETF,
            "crypto": AssetClass.CRYPTO,
            "bond": AssetClass.BOND,
            "commodity": AssetClass.COMMODITY,
            "cash": AssetClass.CASH,
        }
        return mapping.get(asset_class.lower(), AssetClass.OTHER)

    def _map_sector(self, sector: str) -> Sector:
        mapping = {
            "technology": Sector.TECHNOLOGY,
            "healthcare": Sector.HEALTHCARE,
            "financial": Sector.FINANCIAL,
            "consumer": Sector.CONSUMER,
            "energy": Sector.ENERGY,
            "industrial": Sector.INDUSTRIAL,
            "utilities": Sector.UTILITIES,
            "real_estate": Sector.REAL_ESTATE,
            "communication": Sector.COMMUNICATION,
            "materials": Sector.MATERIALS,
        }
        return mapping.get(sector.lower(), Sector.OTHER)
