"""Import Required Dependencies"""
import requests as rq
from .config import config
from .prompts import prompts

class OpenAI:
    """OpenAI compatible API caller"""
    
    def __init__(self,
        api_key: str = config['api_key'],
        base_url: str = config['base_url'],
        model:str=config['model']
    ):
        self.api_key = api_key,
        self.base_url = base_url,
        self.model = model,
    
    def ask(self,prompt:str):
        """Module That sends request to configured provider"""
        
        url = f'{self.base_url}/v1/chat/completions'
        headers = {
            "Authorization":f'Bearer {self.api_key}',
            "Content-Type":"application/json"
        }
        palyload={
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