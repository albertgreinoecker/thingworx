'''
How to retrieve and set properties in ThingWorx using Python
'''

import requests
from dotenv import load_dotenv
import os

load_dotenv()

app_key = os.getenv("APP_KEY")
thingworx_url = os.getenv("THINGWORX_URL")

# Header für Authentifizierung und Format
headers = {
    "AppKey": app_key,
    "Accept": "application/json"
}

def get_property(name):
    url = f"{thingworx_url}Things/test_sensor/Properties/{name}"
    print(url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("rows", [{}])[0].get("temperature", "Keine Daten")
    else:
        print("Fehler beim Abrufen der Daten:", response.status_code, response.text)
        return None

def set_property(name, value):
    url = f"{thingworx_url}Things/test_sensor/Properties/{name}"
    response = requests.put(url, headers=headers, json={name: value})
    if response.status_code == 200:
        print("Property updated successfully!")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == '__main__':
    val = get_property("temperature")
    print(val)
    set_property("temperature", 25)