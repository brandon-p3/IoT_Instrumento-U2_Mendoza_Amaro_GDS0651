from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/KY-022"


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

# Definir el pin donde está conectado el sensor KY-022
sensor_ir = Pin(15, Pin.IN)  # Cambia el GPIO si usas otro

print("Esperando señal infrarroja...")

while True:
    if sensor_ir.value() == 0:  # Cuando recibe señal IR, el sensor KY-022 pone la salida en LOW (0)
        print("¡Señal infrarroja detectada!")
        client.publish(MQTT_TOPIC, "1")
        time.sleep(0.5)  # Evitar detecciones continuas