from openai import OpenAI
from models.model_client import ModelClient


class OpenAIClient(ModelClient):

    def __init__(self, model_name="gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model_name

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content