from dotenv import load_dotenv
import requests, os

load_dotenv()
API_URL = os.getenv("API_URL")

response = requests.get(f"{API_URL}/tables")
print(response.json())
