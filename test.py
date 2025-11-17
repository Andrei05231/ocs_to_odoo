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
        "domain": [["display_name", "ilike", "a%"]],
        "fields": ["display_name"],
        "limit": 20,
    },
)

response.raise_for_status()
data = response.json()
print(data)

