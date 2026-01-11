from dataclasses import dataclass, field
from enum import Enum
from typing import List


class AssetClass(Enum):
    STOCK = "stock"
    ETF = "etf"
    CRYPTO = "crypto"
    BOND = "bond"
    COMMODITY = "commodity"
    CASH = "cash"
    OTHER = "other"


class Sector(Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCIAL = "financial"
    CONSUMER = "consumer"
    ENERGY = "energy"
    INDUSTRIAL = "industrial"
    UTILITIES = "utilities"
    REAL_ESTATE = "real_estate"
    COMMUNICATION = "communication"
    MATERIALS = "materials"
    OTHER = "other"


@dataclass
class Position:
    ticker: str
    quantity: float
    avg_price: float
    current_price: float
    asset_class: AssetClass
    sector: Sector
    
    @property
    def market_value(self) -> float:
        return self.current_price * self.quantity
    
    @property
    def cost_basis(self) -> float:
        return self.avg_price * self.quantity
    
    @property
    def pnl(self) -> float:
        return self.market_value - self.cost_basis


@dataclass
class Portfolio:
    positions: List[Position] = field(default_factory=list)
    
    @property
    def total_value(self) -> float:
        return sum(p.market_value for p in self.positions)
    
    @property
    def total_cost_basis(self) -> float:
        return sum(p.cost_basis for p in self.positions)
    
    @property
    def total_pnl(self) -> float:
        return self.total_value - self.total_cost_basis
    
    def get_positions_by_asset_class(self, asset_class: AssetClass) -> List[Position]:
        return [pos for pos in self.positions if pos.asset_class == asset_class]
    
    def get_positions_by_sector(self, sector: Sector) -> List[Position]:
        return [pos for pos in self.positions if pos.sector == sector]
    
    def get_top_positions(self, limit: int = 10) -> List[Position]:
        return sorted(self.positions, key=lambda x: x.market_value, reverse=True)[:limit]
