"""Main entry point for the portfolio assessment application.
Following DDD, this is the composition root where dependencies are wired.
"""
from infrastructure.trading212_api import Trading212Client
from infrastructure.openai_client import OpenAIAgent
from application.get_portfolio import get_portfolio
from application.assess_portfolio import assess_portfolio
from config.constants import (
    TRADING_212_BASE_URL,
    TRADING_212_ACCESS_KEY,
    TRADING_212_SECRET_KEY,
    OPENAI_API_KEY,
)


def main():
    # Composition root: wire up infrastructure implementations
    # Following DDD, we inject concrete implementations at the application boundary
    
    # Check if using mock mode
    import os
    use_mock = os.environ.get('MOCK_TRADING212', 'false').lower() == 'true'
    
    # Validate required configuration (skip if using mock)
    if not use_mock:
        if not TRADING_212_BASE_URL:
            print("Error: TRADING_212_BASE_URL is not set.")
            print("Please set it in your .env file or environment variables.")
            print("Or set MOCK_TRADING212=true to use mock data for testing.")
            return
        
        if not TRADING_212_ACCESS_KEY or not TRADING_212_SECRET_KEY:
            print("Error: Trading212 credentials are not set.")
            print("Please set TRADING212_STORAGE_ACCESS_KEY and TRADING212_SECRET_STORAGE_ACCESS_KEY in your .env file.")
            print("Or set MOCK_TRADING212=true to use mock data for testing.")
            return
    
    # Use empty strings for mock mode (they won't be used)
    portfolio_repository = Trading212Client(
        base_url=TRADING_212_BASE_URL or "https://placeholder.com",
        access_key=TRADING_212_ACCESS_KEY or "",
        secret_key=TRADING_212_SECRET_KEY or "",
    )

    # Application use cases depend on domain abstractions (interfaces)
    portfolio = get_portfolio(portfolio_repository)
    
    # Validate OpenAI configuration
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is not set.")
        print("Please set it in your .env file or environment variables.")
        return
    
    # Create LLM service (infrastructure)
    llm_service = OpenAIAgent(
        system_prompt="You are a professional portfolio risk and allocation analyst."
    )
    
    # Use case depends on protocol, not concrete implementation
    assessment = assess_portfolio(portfolio, llm_service)

    print("Initial assessment complete.\n")

    while True:
        question = input("Ask the agent (or 'exit'): ")
        if question.lower() == "exit":
            break
        answer = assessment.ask(question)
        print("\n", answer, "\n")


if __name__ == "__main__":
    main()

