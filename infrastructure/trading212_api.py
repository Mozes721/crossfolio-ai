import base64
import requests
from domain.models import Portfolio, Position, AssetClass, Sector


class Trading212Client:
    def __init__(self, api_key: str, secret_key: str | None = None, base_url: str | None = None):
        if secret_key:
            credentials = f"{api_key}:{secret_key}"
            self.auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"
        else:
            self.auth_header = api_key if api_key.startswith("Basic ") else f"Basic {api_key}"
        
        host = "demo.trading212.com" if base_url and "demo" in base_url.lower() else "live.trading212.com"
        self.base_url = f"https://{host}/api/v0"

    def get_portfolio(self) -> Portfolio:
        endpoint = f"{self.base_url}/equity/portfolio"
        response = requests.get(endpoint, headers={"Authorization": self.auth_header})
        response.raise_for_status()
        raw_positions = response.json()
        return self._convert_to_domain_portfolio(raw_positions)

    def _convert_to_domain_portfolio(self, raw_positions: list) -> Portfolio:
        positions = []
        
        for pos_data in raw_positions:
            position = Position(
                ticker=pos_data.get("ticker", ""),
                quantity=float(pos_data.get("quantity", 0)),
                avg_price=float(pos_data.get("averagePrice", 0)),
                current_price=float(pos_data.get("currentPrice", 0)),
                asset_class=self._map_asset_class(pos_data.get("asset_class")),
                sector=self._map_sector(pos_data.get("sector"))
            )
            positions.append(position)
        
        return Portfolio(positions=positions)

    def _map_asset_class(self, asset_class: str) -> AssetClass:
        mapping = {
            "stock": AssetClass.STOCK,
            "etf": AssetClass.ETF,
            "crypto": AssetClass.CRYPTO,
            "bond": AssetClass.BOND,
            "commodity": AssetClass.COMMODITY,
            "cash": AssetClass.CASH,
        }
        return mapping.get(str(asset_class).lower(), AssetClass.OTHER)

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
        return mapping.get(str(sector).lower(), Sector.OTHER)
