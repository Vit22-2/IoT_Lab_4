import network, time, json
from umqtt.simple import MQTTClient
from machine import Pin, I2C
from bmp280 import BMP280   # ← use bmp280.py driver

# ---------- Wi-Fi ----------
SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

# ---------- MQTT ----------
BROKER = "test.mosquitto.org"
PORT = 1883
CLIENT_ID = b"esp32_bmp280_1"
TOPIC = b"/aupp/group1m/IOTLab"
KEEPALIVE = 30

# ---------- I2C Setup ----------
# Default pins for ESP32: SDA=21, SCL=22
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sensor = BMP280(i2c)

# ---------- Constants ----------
SEA_LEVEL_PRESSURE = 1013.25  # hPa (adjust if you know local pressure)

# ---------- Functions ----------
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > 20000:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.3)
    print("Wi-Fi connected:", wlan.ifconfig())
    return wlan

def make_client():
    return MQTTClient(client_id=CLIENT_ID, server=BROKER, port=PORT, keepalive=KEEPALIVE)

def connect_mqtt(c):
    time.sleep(0.5)
    c.connect()
    print("MQTT connected")

# ---------- Main Loop ----------
def main():
    wifi_connect()
    client = make_client()
    while True:
        try:
            connect_mqtt(client)
            while True:
                # Read temperature (°C) and pressure (Pa)
                temperature = sensor.temperature
                pressure_pa = sensor.pressure
                pressure_hpa = pressure_pa / 100.0  # convert Pa → hPa

                # Calculate altitude (m)
                altitude = 44330 * (1 - (pressure_hpa / SEA_LEVEL_PRESSURE) ** 0.1903)

                # Build JSON payload
                payload = json.dumps({
                    "temperature": round(temperature, 2),
                    "pressure": round(pressure_hpa, 2),
                    "altitude": round(altitude, 2)
                })

                # Publish data
                client.publish(TOPIC, payload)
                print("Sent:", payload)
                time.sleep(5)

        except OSError as e:
            print("MQTT error:", e)
            try:
                client.close()
            except:
                pass
            print("Retrying MQTT in 3s...")
            time.sleep(3)

# ---------- Run ----------
main()
