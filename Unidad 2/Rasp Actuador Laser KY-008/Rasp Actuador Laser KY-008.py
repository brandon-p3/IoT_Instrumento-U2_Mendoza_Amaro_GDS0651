from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/actuador/KY-008"


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

LASER_PIN = 2  # GPIO donde conectaste el KY-008

laser = Pin(LASER_PIN, Pin.OUT)  # Configurar el pin como salida

while True:
    laser.on()
    mensaje = 1
    print("Láser encendido")
    client.publish(MQTT_TOPIC, str(mensaje))
    time.sleep(5)
    
    laser.off()
    mensaje= 2
    print("Láser apagado")
    client.publish(MQTT_TOPIC, str(mensaje))
    time.sleep(5)
    
