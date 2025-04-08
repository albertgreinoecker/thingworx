import requests
from dotenv import load_dotenv
import os

load_dotenv()

app_key = os.getenv("APP_KEY")
thingworx_url = os.getenv("THINGWORX_URL")

print(app_key)
print(thingworx_url)

# Header für Authentifizierung und Format
headers = {
    "AppKey": app_key,
    "Accept": "application/json"
}

# HTTP-GET an ThingWorx
response = requests.get(thingworx_url, headers=headers)

# Antwort prüfen
if response.status_code == 200:
    data = response.json()
    print("Aktuelle Temperatur:", data.get("Temperature"))
else:
    print("Fehler beim Abrufen der Daten:", response.status_code, response.text)
