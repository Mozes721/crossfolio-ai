from abc import ABC, abstractmethod
from entities import Portfolio


class PortfolioRepository(ABC):
    @abstractmethod
    def get_portfolio(self) -> Portfolio:
        pass
