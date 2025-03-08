from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/KY-025"


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

# Definir el pin de la salida digital del KY-025
sensor_pin = Pin(15, Pin.IN)  # Cambia el pin según tu configuración

print("Esperando detección de campo magnético...")

while True:
    # Leer el valor digital del sensor (0 o 1)
    sensor_value = sensor_pin.value()
    
    if sensor_value == 1:
        print("Campo magnético detectado")
        client.publish(MQTT_TOPIC, "1")
    else:
        print("No hay campo magnético")
    
    # Esperar un poco antes de la siguiente lectura
    time.sleep(1)
