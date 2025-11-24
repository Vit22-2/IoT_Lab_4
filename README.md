# IoT_Lab4

## Features

- Publish random integer values from the ESP32 using MicroPython
- Send data to an MQTT broker (test.mosquitto.org)
- Receive and process MQTT data using Node-RED
- Store IoT data in InfluxDB (time-series database)
- Visualize real-time values on a Grafana Dashboard
- Demonstrate a complete IoT workflow:
ESP32 → MQTT → Node-RED → InfluxDB → Grafana

## Requirements

### Hardware
- ESP32 (MicroPython firmware installed)
- USB Cable + Laptop
- Stable Wi-Fi connection

### Software
- Thonny IDE / mpremote / ampy
- MicroPython firmware uploaded to ESP32
- Node-RED (for IoT automation)
- InfluxDB 1.x (database for time-series data)
- Grafana (dashboard visualization)
- MQTT Explorer (optional for monitoring MQTT topics)

## Wiring

<img width="1602" height="847" alt="image" src="https://github.com/user-attachments/assets/e0c4b477-2dc7-4d45-b7c6-955aa09b8233" />

## Usage Instructions

- Upload Code to ESP32
   - In Thonny, open and upload your MicroPython script to the ESP32.
   - Run the code.
   - The ESP32 will begin publishing random integer values every 5 seconds.
- MQTT Testing
   - Open MQTT Explorer.
   - Connect to test.mosquitto.org.
   - Search for your topic: /aupp/esp32/random
   - You will see new values appearing every 5 seconds from the ESP32.
- Node-RED Flow
   - Open Node-RED at http://localhost:1880
   - Verify that the MQTT In → Debug nodes show live incoming data.
   - Add the Function node and InfluxDB Out node to forward data into the database.
- InfluxDB Data Verification
   - Open the InfluxDB shell.
   - Run: SELECT * FROM random ORDER BY time DESC LIMIT 5;
   - You will see the latest values stored from Node-RED.
- Grafana Dashboard
   - Log in to Grafana at http://localhost:3000
   - Add your InfluxDB data source.
   - Create a dashboard panel using:
   - SELECT value FROM random
   - Watch real-time updates as the ESP32 publishes new random data.
   - Use this workflow to demonstrate a full IoT pipeline from the ESP32 all the way to a live dashboard in Grafana.

## Screenshots

## Short Demo Video (60–90s)
