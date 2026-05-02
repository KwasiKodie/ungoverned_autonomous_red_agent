import os
from anthropic import Anthropic
from models.model_client import ModelClient
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient(ModelClient):

    def __init__(self, model_name="claude-opus-4-5-20251101"):
        api_key = os.getenv("CLAUDE_API_KEY")

        if not api_key:
            raise ValueError("CLAUDE_API_KEY not set in environment")

        self.client = Anthropic(api_key=api_key)
        self.model = model_name

    def generate(self, prompt: str) -> str:

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.content[0].text