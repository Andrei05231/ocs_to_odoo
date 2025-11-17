from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("API_KEY")
target_id = 175
display_name = "Updated again"
hostname = os.getenv("HOST")
model = "x_computer"

response = requests.post(
    f"http://{hostname}/json/2/{model}/write",
    headers={
        "Authorization": f"Bearer {api_key}",
        # "X-Odoo-Database": "...",
    },
    json={
        "ids": [
            target_id
        ],
        "vals": {
            "x_name": display_name
        }
    },
)
response.raise_for_status()
data = response.json()
print(data)

