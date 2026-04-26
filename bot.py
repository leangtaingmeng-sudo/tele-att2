
from httpcore import request
import requests
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Agent():
    model: str = "qwen2.5-coder-0.5b-instruct-f1"
    base_url: str = "http://127.0.0.1:1234/v1"
    api:str = field(default="No_API_Key", repr=False)
    message:list[dict[str:Any]] = field(default_factory = list)

    def __post_init__(self)->None:
       self.base_url = self.base_url.rstrip("/")

    def chat(self, user_message:str)->str:
        self.message.append({"role": "user", "content": user_message})
        url = f"{self.base_url}/chat/completions"
        headers = {
            "authorization": f"bearer {self.api}",
            "content_type": "json/application"
        }
        response = requests.post(
            url,
            headers=headers,
            json = {'Model': self.model, "messages": self.message}
        )
        data = response.json()
        data = data.get("choices")
        message = data[0].get("message")
        self.message.append({"role": 'assistance', "content": {message}})
        return message.get("content")
