from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "KAREN 8870"
PASSWORD = "e*905F06"
MQTT_BROKER = "192.168.137.41"
MQTT_TOPIC = "gds0651/sensor/KY-32"

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

# Definir el pin del sensor
SENSOR_PIN = 15  # Puedes cambiarlo según tu conexión
sensor = Pin(SENSOR_PIN, Pin.IN)

while True:
    if sensor.value() == 1:
        print("Objeto detectado 🚨")
        client.publish(MQTT_TOPIC, "1")
    else:
        print("No hay objeto")
    
    time.sleep(3)  # Pequeña pausa para evitar demasiadas lecturas
