import requests 
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from .env file
load_dotenv()

deep_seek_api_key = os.getenv('DEEP-SEEK-API')

def deepseek_api():
    # Connect to DeepSeek API
    pass