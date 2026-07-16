"""Import Required Dependencies"""
from config import config
from prompts import prompts
from typing import Any
import json
import httpx

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

    def ask(self,prompt:str) -> Any:
        """Module That sends request to configured provider"""

        url = f'{self.base_url}/v1/chat/completions'
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

        res = httpx.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content'],  res.json()['model']

        return json.dumps(res.json(),indent=4)
