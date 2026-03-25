import json
import time
import random
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

BROKER_HOST = os.getenv("THINGWORX_MQTT")  # ThingWorxx Broker-Adresse
BROKER_PORT = 443
USERNAME =  os.getenv("THINGWORX_USER")
PASSWORD =  os.getenv("THINGWORX_USER_PW")
CLIENT_ID = "publisher-demo-01"

TOPIC = "thingworxx/demo/sensor"  # Topic anpassen
QOS = 1  # 0 = fire & forget, 1 = at least once, 2 = exactly once
INTERVAL = 5


def on_connect(client, userdata, flags, reason_code, properties=None):
    """Callback: wird aufgerufen sobald die Verbindung hergestellt ist."""
    if reason_code == 0:
        print(f"[✓] Verbunden mit Broker: {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"[✗] Verbindung fehlgeschlagen. Reason code: {reason_code}")


def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """Callback: wird aufgerufen wenn eine Nachricht erfolgreich gesendet wurde."""
    print(f"    → Nachricht bestätigt (mid={mid})")


def on_disconnect(client, userdata, flags, reason_code, properties=None):
    """Callback: wird aufgerufen beim Trennen der Verbindung."""
    print(f"[i] Verbindung getrennt (reason_code={reason_code})")


def build_payload(counter: int) -> str:
    """Erstellt eine JSON-Payload mit Simulationsdaten."""
    payload = {
        "counter": counter,
        "temperature": round(random.uniform(18.0, 26.0), 2),
        "humidity": round(random.uniform(40.0, 70.0), 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return json.dumps(payload)


def main():
    # Client erstellen (MQTT v5 – für ältere Broker ggf. MQTTv311 verwenden)

    client = mqtt.Client(
        client_id=CLIENT_ID,
        protocol=mqtt.MQTTv5,
        transport="websockets",
    )
    client.ws_set_options(path="/Thingworx/WS")
    client.username_pw_set(USERNAME, PASSWORD)
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)



    # Callbacks registrieren
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Optional: TLS aktivieren (Port 8883)
    # client.tls_set()

    print(f"[i] Verbinde mit {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    # Netzwerk-Loop im Hintergrund starten
    client.loop_start()

    counter = 0
    try:
        while True:
            counter += 1
            payload = build_payload(counter)
            result = client.publish(TOPIC, payload, qos=QOS)

            print(f"[↑] Sende #{counter} auf Topic '{TOPIC}'")
            print(f"    Payload: {payload}")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n[i] Abbruch durch Benutzer.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[i] Verbindung sauber geschlossen.")


if __name__ == "__main__":
    main()