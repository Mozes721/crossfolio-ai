from openai import OpenAI
from typing import Any


class OpenAIAgent:
    def __init__(self, system_prompt: str = "You are a helpful assistant."):
        if not hasattr(OpenAIAgent, 'api_key'):
            from config.constants import OPENAI_API_KEY
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is not set")
            OpenAIAgent.api_key = OPENAI_API_KEY
        
        self.client = OpenAI(api_key=OpenAIAgent.api_key)
        self.system_prompt = system_prompt
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]

    def ask(self, question: str) -> str:
        self.conversation_history.append({"role": "user", "content": question})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=1000
            )
            answer = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            raise ConnectionError(f"Failed to get response from OpenAI: {e}")
