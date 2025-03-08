import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-032"


# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi!")

# Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("✅ Conectado a MQTT!")


SENSOR_PIN = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if SENSOR_PIN.value() == 0:
        print("Obstacle detected")
        client.publish(MQTT_TOPIC, str(SENSOR_PIN.value()))
    else:
        print("No obstacle")
    time.sleep(0.5)