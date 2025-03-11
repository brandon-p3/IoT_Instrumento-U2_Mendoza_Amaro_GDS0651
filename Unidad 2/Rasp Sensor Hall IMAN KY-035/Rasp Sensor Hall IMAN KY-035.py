from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-035"


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


# Configurar el pin analógico (GPIO34 en ESP32)
sensor_hall = ADC(Pin(34))
sensor_hall.atten(ADC.ATTN_11DB)  # Ajusta la atenuación para leer hasta 3.3V

while True:
    valor = sensor_hall.read()  # Leer valor analógico (0 - 4095 en ESP32)
    print("Valor del sensor KY-035:", valor)
    if valor > 0:
        client.publish(MQTT_TOPIC, str(valor))
    
    time.sleep(0.5)  # Pequeña pausa para no saturar la salida
