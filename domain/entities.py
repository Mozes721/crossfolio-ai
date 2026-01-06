from dataclasses import dataclass, field
from typing import List

from .value_objects import Money, Price, Quantity, Ticker, AssetClass, Sector


@dataclass
class Position:
    ticker: Ticker
    quantity: Quantity
    avg_price: Price
    current_price: Price
    asset_class: AssetClass
    sector: Sector

    @property
    def market_value(self) -> Money:
        return Money(amount=self.current_price.value * self.quantity.value)

    @property
    def cost_basis(self) -> Money:
        return Money(amount=self.avg_price.value * self.quantity.value)

    @property
    def pnl(self) -> Money:
        return Money(amount=self.market_value.amount - self.cost_basis.amount)


@dataclass
class Portfolio:
    positions: List[Position] = field(default_factory=list)

    @property
    def total_value(self) -> Money:
        return Money(amount=sum(pos.market_value.amount for pos in self.positions))

    @property
    def total_cost_basis(self) -> Money:
        return Money(amount=sum(pos.cost_basis.amount for pos in self.positions))

    @property
    def total_pnl(self) -> Money:
        return Money(amount=self.total_value.amount - self.total_cost_basis.amount)

    def add_position(self, position: Position):
        self.positions.append(position)

    def get_positions_by_asset_class(self, asset_class: AssetClass) -> List[Position]:
        return [pos for pos in self.positions if pos.asset_class == asset_class]

    def get_positions_by_sector(self, sector: Sector) -> List[Position]:
        return [pos for pos in self.positions if pos.sector == sector]

    def get_top_positions(self, limit: int = 10) -> List[Position]:
        return sorted(self.positions, key=lambda x: x.market_value.amount, reverse=True)[:limit]
