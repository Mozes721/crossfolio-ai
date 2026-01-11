import os
from dotenv import load_dotenv
from openrouter import OpenRouter
from domain.models import Portfolio

load_dotenv()


class LLMService:
    """Simplified LLM service following OpenRouter SDK pattern."""
    
    def __init__(self, system_prompt: str = "You are a helpful assistant.", model: str = "openai/gpt-4o-mini", portfolio: Portfolio | None = None):
        self.client = OpenRouter(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        
        if portfolio:
            # Format positions as a simple list with calculated values
            positions_list = []
            for i, pos in enumerate(portfolio.positions, 1):
                positions_list.append(
                    f"{i}. {pos.ticker}: {pos.quantity} shares @ ${pos.current_price:.2f}/share = ${pos.market_value:.2f}"
                )
            
            portfolio_summary = (
                f"My portfolio (all values in USD):\n"
                f"Total portfolio value: ${portfolio.total_value:.2f}\n"
                f"Number of positions: {len(portfolio.positions)}\n\n"
                f"Positions:\n" + "\n".join(positions_list) + "\n\n"
                f"Note: All market values are pre-calculated. Use the values shown above."
            )
            self.messages.append({"role": "user", "content": portfolio_summary})

    def ask(self, question: str, model: str | None = None) -> str:
        self.messages.append({"role": "user", "content": question})
        
        response = self.client.chat.send(
            model=model or self.model,
            messages=self.messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer
