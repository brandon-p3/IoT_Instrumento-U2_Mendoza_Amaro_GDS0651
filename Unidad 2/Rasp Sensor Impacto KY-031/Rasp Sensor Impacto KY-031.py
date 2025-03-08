import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-031"


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


# Configuración del sensor de impacto (GPIO 15)
impact_sensor = Pin(15, Pin.IN)

while True:
    estado_actual = impact_sensor.value()  # Leer estado del sensor
    print("",estado_actual)
    
    if estado_actual == 1:
        client.publish(MQTT_TOPIC, str(estado_actual))
        
    time.sleep(1)  # Pequeña espera para evitar falsos positivos