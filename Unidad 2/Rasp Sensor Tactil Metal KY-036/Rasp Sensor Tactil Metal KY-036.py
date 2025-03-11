from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-036"


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



# Configuración del pin digital (DO) del KY-036
sensor_metal = Pin(14, Pin.IN)  # GPIO 14 o el pin digital que estés usando



while True:
    # Leer la salida digital del sensor (0 o 1)
    detecta_metal = sensor_metal.value()
    
    if detecta_metal == 1:
        print("¡Metal detectado!")
        client.publish(MQTT_TOPIC, str(detecta_metal))
    else:
        print("No se detecta metal.")


    # Esperar un poco antes de la siguiente lectu
    time.sleep(0.5)
