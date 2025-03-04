from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/KY-021"


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

# Definir el pin del sensor (cambia según tu microcontrolador)
KY021_PIN = 16  # GPIO16 en ESP32 (ajústalo si usas otro pin)
sensor = Pin(KY021_PIN, Pin.IN)

while True:
    estado = sensor.value()  # Leer el estado del sensor
    if estado == 0:
        print("🔵 Campo magnético detectado (Reed Cerrado)")
    else:
        print("⚫ Sin campo magnético (Reed Abierto)")
    
    client.publish(MQTT_TOPIC, str(estado))
    time.sleep(5)  # Pequeña pausa para evitar lecturas constantes

