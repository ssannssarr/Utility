"""Iport Required Dependencies"""
import os

config = {
    'api_key':os.getenv('OPENROUTER_API_KEY'),
    'model':'openrouter/free',
    'base_url':'https://openrouter.ai/api'
}
