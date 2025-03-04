from machine import Pin
import time
import math
import network
from umqtt.simple import MQTTClient


# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/Ky-010"

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

sensor = Pin(4, Pin.IN) 

while True:
    estado = sensor.value()
    if estado == 0:  # El haz está interrumpido
        client.publish(MQTT_TOPIC, str(estado))
        print("Interrupción detectada")
    else:
        client.publish(MQTT_TOPIC, str(estado))
        print("No hay interrupción")
    time.sleep(5)  # Espera 500 ms antes de leer nuevamente
    

