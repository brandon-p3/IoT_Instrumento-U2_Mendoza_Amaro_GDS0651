from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

sensor = Pin(5, Pin.IN)  # Pin GPIO donde está conectado el KY-002

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/Ky-002"

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




while True:
    if sensor.value() == 1:  # Se detecta una vibración cuando el circuito se cierra momentáneamente
        movimiento = 1
        print("¡Vibración detectada!", movimiento)
        
    else:
        movimiento = 0
        print("No hay anda!", movimiento)
        
        
        
    client.publish(MQTT_TOPIC, str(movimiento))
    time.sleep(5)  # Pequeña pausa para evitar múltiples detecciones por la misma vibración