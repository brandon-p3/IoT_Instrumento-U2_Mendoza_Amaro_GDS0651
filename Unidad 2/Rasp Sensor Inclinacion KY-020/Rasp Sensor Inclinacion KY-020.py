from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-020"


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


# Configuración del pin del sensor de inclinación KY-020
sensor_inclinacion = Pin(34, Pin.IN, Pin.PULL_UP)  # GPIO34, con pull-up interno

# Función para leer el estado del sensor de inclinación
def leer_inclinacion():
    if sensor_inclinacion.value() == 0:  # Estado bajo (sensor activado, sensor inclinado)
        print("¡Sensor de inclinación activado! El sensor está inclinado.")
        client.publish(MQTT_TOPIC, str(sensor_inclinacion.value()))
    else:  # Estado alto (sensor no activado, sensor horizontal)
        print("El sensor está en posición horizontal.")

# Bucle principal para leer el estado del sensor cada segundo
while True:
    leer_inclinacion()
    time.sleep(1)  # Leer cada segundo
