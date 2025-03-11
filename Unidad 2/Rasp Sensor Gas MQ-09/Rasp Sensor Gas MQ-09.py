from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/MQ-09"


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



# Configuración del pin digital (DOUT) del MQ-9
pin_digital = Pin(13, Pin.IN)  # GPIO 13 o el pin digital que estés usando

while True:
    # Leer la salida digital (0 o 1)
    detecta_gas = pin_digital.value()
    
    if detecta_gas == 1:
        print("¡Gas detectado!")
        client.publish(MQTT_TOPIC, str(detecta_gas))
    else:
        print("No se detecta gas.")
    
    # Pausa para evitar saturar el monitor serie
    time.sleep(1)

