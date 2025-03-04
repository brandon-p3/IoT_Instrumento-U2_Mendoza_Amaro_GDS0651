import time
from machine import Pin
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/KY-024"


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


# Configurar el pin digital D0
KY024_D0_PIN = 15  # Cambia según el GPIO que uses
sensor_digital = Pin(KY024_D0_PIN, Pin.IN)

while True:
    state = sensor_digital.value()  # 0 = Campo magnético detectado, 1 = No detectado
    if(state == 0):
        client.publish(MQTT_TOPIC, "1")
        
    print("⚡ Campo Magnético Detectado" if state == 0 else "🔹 Sin campo magnético")
    time.sleep(1)  # Leer cada 1 segundo
