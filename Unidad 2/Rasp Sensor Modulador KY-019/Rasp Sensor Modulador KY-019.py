from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/KY-019"


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

# Definir el pin donde está conectado el sensor KY-022 (sensor IR)
sensor_ir = Pin(15, Pin.IN) 

# Definir el pin donde está conectado el relé KY-019 (para controlar el foco)
relay_pin = Pin(2, Pin.OUT) 

# Inicializar el relé apagado (en LOW, el relé está apagado)
relay_pin.value(0)

print("Esperando señal infrarroja...")

while True:
    if sensor_ir.value() == 0:  # Cuando recibe señal IR, el sensor KY-022 pone la salida en LOW (0)
        print("¡Señal infrarroja detectada!")
        client.publish(MQTT_TOPIC, "1")
        relay_pin.value(1)  # Enciende el relé (prende el foco)
        time.sleep(2)  # Mantén el foco encendido por 2 segundos
        relay_pin.value(0)  # Apaga el relé (apaga el foco)
        time.sleep(0.5)  # Evitar detecciones continuas

