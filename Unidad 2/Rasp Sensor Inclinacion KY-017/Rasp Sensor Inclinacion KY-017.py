from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-017"


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


# Configuración del pin del sensor de inclinación
sensor_inclinacion = Pin(34, Pin.IN, Pin.PULL_UP)  # GPIO34

# Función para leer el estado del sensor
def leer_inclinacion():
    valor = sensor_inclinacion.value()
    if  valor == 0:  # Estado bajo (sensor activado)
        print("¡Sensor de inclinación activado! El módulo está inclinado.")
        client.publish(MQTT_TOPIC, str(valor))
        
    else:  # Estado alto (sensor desactivado)
        print("El módulo está en posición horizontal.")

# Bucle principal para leer el estado del sensor cada segundo
while True:
    leer_inclinacion()
    time.sleep(1)  # Leer cada segundo

