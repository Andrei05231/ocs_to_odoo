from dotenv import load_dotenv
import os
import requests

# Load .env file
load_dotenv()

api_key = os.getenv("API_KEY")

response = requests.post(
    "http://odoo.artehnis.local/json/2/x_computer/search_read",
    headers={
        "Authorization": f"Bearer {api_key}",
        # "X-Odoo-Database": "...",
    },
    json={
        # "domain": [["display_name", "ilike", "a%"]],
        "domain":[],
        "fields": ["x_name"],
        "limit": 50,
    },
)

response.raise_for_status()
data = response.json()
print(data)

