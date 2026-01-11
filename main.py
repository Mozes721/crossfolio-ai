import argparse
import os
from dotenv import load_dotenv
from infrastructure.trading212_api import Trading212Client
from infrastructure.kraken_api import KrakenClient
from infrastructure.openai_client import LLMService

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='Portfolio Assessment Tool')
    parser.add_argument('--crypto', action='store_true', help='Use Kraken for crypto portfolio')
    parser.add_argument('--stock', action='store_true', help='Use Trading212 for stock portfolio')
    
    args = parser.parse_args()
    
    if args.crypto:
        portfolio_client = KrakenClient(
            api_key=os.getenv("KRAKEN_API_KEY"),
            private_key=os.getenv("KRAKEN_PRIVATE_KEY")
        )
        system_prompt = "You are a professional portfolio risk and allocation analyst on cryptocurrencies."
    elif args.stock:
        portfolio_client = Trading212Client(
            api_key=os.getenv("TRADING_212_ACCESS_KEY"),
            secret_key=os.getenv("TRADING_212_SECRET_STORAGE_ACCESS_KEY"),
            base_url=os.getenv("TRADING_212_BASE_URL"),
        )
        system_prompt = "You are a professional portfolio risk and allocation analyst on stocks and ETFs."
    else:
        print("Error: Please specify either --crypto or --stock")
        parser.print_help()
        return
    
    portfolio = portfolio_client.get_portfolio()
    
    print(f"Portfolio loaded: {len(portfolio.positions)} positions")
    print(f"Total value: ${portfolio.total_value:,.2f}\n")
    
    # Initialize LLM service with portfolio context
    llm_service = LLMService(
        system_prompt=system_prompt,
        model="openai/gpt-4o-mini",
        portfolio=portfolio
    )
    
    # Interactive Q&A loop
    while True:
        question = input("Ask about your portfolio (or 'exit'): ")
        if question.lower() == "exit":
            break
        
        try:
            answer = llm_service.ask(question)
            print(f"\n{answer}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()

