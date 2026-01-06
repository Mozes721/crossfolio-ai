from typing import Any


class PortfolioAssessment:
    def __init__(self, llm_service: Any):
        self.llm_service = llm_service

    def ask(self, question: str) -> str:
        return self.llm_service.ask(question)


def assess_portfolio(portfolio, llm_service: Any) -> PortfolioAssessment:
    return PortfolioAssessment(llm_service)
