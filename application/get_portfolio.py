from domain.repositories import PortfolioRepository
from domain.entities import Portfolio


def get_portfolio(repository: PortfolioRepository) -> Portfolio:
    return repository.get_portfolio()
