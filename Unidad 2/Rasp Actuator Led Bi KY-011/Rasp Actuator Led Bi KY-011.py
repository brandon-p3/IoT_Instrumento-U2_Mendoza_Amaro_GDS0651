from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/actuador/KY-011"


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


# Configuración de los pines para los LEDs
led_red = Pin(2, Pin.OUT)  # Pin para el LED rojo
led_green = Pin(4, Pin.OUT)  # Pin para el LED verde

while True:
    # Encender LED rojo y apagar LED verde
    led_red.value(1)  # Rojo encendido
    led_green.value(0)  # Verde apagado
    led = 1
    client.publish(MQTT_TOPIC, str(led))
    print("Rojo")
    time.sleep(3)  # Esperar 3 segundos
    
    # Apagar LED rojo y encender LED verde
    led_red.value(0)  # Rojo apagado
    led_green.value(2)  # Verde encendido
    led = 2
    client.publish(MQTT_TOPIC, str(led))
    print("Verde")
    time.sleep(3)  # Esperar 3 segundos
