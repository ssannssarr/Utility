"""Import Required Dependencies"""
from typing import Any
import json
import httpx
from .config import config
from .prompts import prompts

class OpenAI:
    """OpenAI compatible API caller"""

    def __init__(self,
        api_key: str = config['api_key'],
        base_url: str = config['base_url'],
        model:str = config['model']
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = httpx.Client(base_url=self.base_url,timeout=None)

    def ask(self,prompt:str) -> Any:
        """Module That sends request to configured provider"""

        url = '/v1/chat/completions'
        headers = {
            "Authorization":f'Bearer {self.api_key}',
            "Content-Type":"application/json"
        }
        payload={
            "model":self.model,
            "messages":[
               {
                    "role":"system",
                    "content":prompts['system_prompt']
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        }

        res = self.client.post(
            url,
            headers=headers,
            json=payload,
        )

        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content'],  res.json()['model']

        return json.dumps(res.json(),indent=4)
