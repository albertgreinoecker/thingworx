"""
ThingWorxx MQTT Subscriber Demo
=================================
Verbindet sich mit dem ThingWorxx MQTT Broker und empfängt Nachrichten
von einem oder mehreren Topics.

Installation:
    pip install paho-mqtt

Verwendung:
    python mqtt_subscriber.py
"""

import json
import signal
import sys
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import ssl
load_dotenv()

BROKER_HOST = os.getenv("THINGWORX_MQTT")  # ThingWorxx Broker-Adresse
BROKER_PORT = 443
USERNAME =  os.getenv("THINGWORX_USER")
PASSWORD =  os.getenv("THINGWORX_USER_PW")
CLIENT_ID = "publisher-demo-02"

# Ein einzelnes Topic oder Wildcard-Patterns:
#   "thingworxx/demo/#"   → alle Sub-Topics unter demo/
#   "thingworxx/+/sensor" → beliebige zweite Ebene, endet mit /sensor
SUBSCRIPTIONS = [
    ("thingworxx/demo/sensor", 1),   # (topic, QoS)
    ("thingworxx/demo/status", 0),
]
# ──────────────────────────────────────────────


def on_connect(client, userdata, flags, reason_code, properties=None):
    """Callback: wird aufgerufen sobald die Verbindung hergestellt ist."""
    if reason_code == 0:
        print(f"[✓] Verbunden mit Broker: {BROKER_HOST}:{BROKER_PORT}")
        # Topics nach (Re-)Connect abonnieren
        for topic, qos in SUBSCRIPTIONS:
            client.subscribe(topic, qos=qos)
            print(f"[i] Abonniert: '{topic}'  (QoS={qos})")
    else:
        print(f"[✗] Verbindung fehlgeschlagen. Reason code: {reason_code}")


def on_message(client, userdata, msg):
    """Callback: wird aufgerufen wenn eine neue Nachricht eintrifft."""
    raw = msg.payload.decode("utf-8", errors="replace")

    print(f"\n[↓] Nachricht empfangen")
    print(f"    Topic  : {msg.topic}")
    print(f"    QoS    : {msg.qos}")
    print(f"    Retain : {msg.retain}")

    # Versuche JSON zu parsen, sonst Rohtext ausgeben
    try:
        data = json.loads(raw)
        print(f"    Payload: {json.dumps(data, indent=6, ensure_ascii=False)}")

        # Beispiel: auf bestimmte Felder reagieren
        if "temperature" in data and data["temperature"] > 25.0:
            print(f"    ⚠  Temperatur über Schwellwert: {data['temperature']} °C")

    except json.JSONDecodeError:
        print(f"    Payload (raw): {raw}")


def on_subscribe(client, userdata, mid, reason_codes, properties=None):
    """Callback: Bestätigung des Broker über erfolgreiches Subscribe."""
    print(f"[✓] Subscribe bestätigt (mid={mid})")


def on_disconnect(client, userdata, flags, reason_code, properties=None):
    """Callback: wird aufgerufen beim Trennen der Verbindung."""
    print(f"\n[i] Verbindung getrennt (reason_code={reason_code})")


def main():
    # Client erstellen
    client = mqtt.Client(
        client_id=CLIENT_ID,
        protocol=mqtt.MQTTv5,
        transport="websockets"
    )

    # Authentifizierung setzen
    client.username_pw_set(USERNAME, PASSWORD)
    client.ws_set_options(path="/Thingworx/WS")
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

    # Callbacks registrieren
    client.on_connect    = on_connect
    client.on_message    = on_message
    client.on_subscribe  = on_subscribe
    client.on_disconnect = on_disconnect

    # Optional: TLS aktivieren (Port 8883)
    # client.tls_set()

    # Sauberes Beenden bei Ctrl+C
    def _shutdown(sig, frame):
        print("\n[i] Abbruch durch Benutzer.")
        client.loop_stop()
        client.disconnect()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)

    print(f"[i] Verbinde mit {BROKER_HOST}:{BROKER_PORT} ...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print("[i] Warte auf Nachrichten … (Ctrl+C zum Beenden)")
    # Blockierender Loop – hält das Skript am Laufen
    client.loop_forever()


if __name__ == "__main__":
    main()