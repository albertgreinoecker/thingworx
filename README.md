# ThingWorx Python Examples

Small Python examples for connecting to a ThingWorx instance over REST and MQTT.

## Included Examples

- `ex_01_first.py`: reads and updates a property on the `test_sensor` Thing through the ThingWorx REST API
- `ex_02_mqtt_pub.py`: publishes simulated sensor data to a ThingWorx MQTT topic over secure WebSockets
- `ex_02_mqtt_sub.py`: subscribes to MQTT topics and prints incoming messages

## Requirements

- Python 3
- Access to a ThingWorx environment
- A valid ThingWorx AppKey for REST access
- Valid ThingWorx MQTT user credentials

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the required connection settings:

```env
APP_KEY=your_app_key
THINGWORX_URL=https://your-host/Thingworx/
THINGWORX_MQTT=your-mqtt-host
THINGWORX_USER=your_username
THINGWORX_USER_PW=your_password
```

Notes:

- `THINGWORX_URL` should point to the ThingWorx base URL used by the REST example.
- The REST example currently targets the Thing `test_sensor`.
- The MQTT examples connect with `transport="websockets"` on port `443` and use the WebSocket path `/Thingworx/WS`.

## Usage

Run the REST property example:

```bash
python ex_01_first.py
```

Run the MQTT publisher:

```bash
python ex_02_mqtt_pub.py
```

Run the MQTT subscriber:

```bash
python ex_02_mqtt_sub.py
```

## MQTT Topics

The publisher sends messages to:

```text
thingworxx/demo/sensor
```

The subscriber listens to:

```text
thingworxx/demo/sensor
thingworxx/demo/status
```

Adjust topics directly in the Python files if your ThingWorx setup uses different routing.

## Notes

- The MQTT examples currently disable certificate verification via `tls_insecure_set(True)`. That may be acceptable for local testing, but it should be tightened for production use.
- The scripts are simple demos and print status information directly to the console.
