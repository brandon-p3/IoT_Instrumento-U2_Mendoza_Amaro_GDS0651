import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-033"


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


# Definir el pin del sensor de línea (KY-033)
sensor_pin = machine.Pin(13, machine.Pin.IN)  # Cambia al pin que estés utilizando (por ejemplo, GPIO 13)


# Bucle principal
while True:
    # Leer el valor del sensor
    sensor_value = sensor_pin.value()
    
    # Si se detecta la línea (HIGH)
    if sensor_value == 1:
        print("Línea detectada")
        client.publish(MQTT_TOPIC, str(sensor_value))
    else:
        print("No hay línea")
    
    time.sleep(5)  # Pausa de 500 ms entre lecturas
