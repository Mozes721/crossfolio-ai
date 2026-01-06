from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"


@dataclass(frozen=True)
class Price:
    value: float


@dataclass(frozen=True)
class Quantity:
    value: int


@dataclass(frozen=True)
class Ticker:
    symbol: str

    def __post_init__(self):
        if not self.symbol or not isinstance(self.symbol, str):
            raise ValueError("Ticker symbol must be a non-empty string")


from enum import Enum


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
