from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/MQ-03"


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

# Configurar el sensor MQ-3 en el pin 34
mq3 = ADC(Pin(34))
mq3.atten(ADC.ATTN_11DB)  # Permite leer hasta 3.3V (rango 0-4095)

# Bucle principal
while True:
    valor_adc = mq3.read()  # Leer el valor del sensor

    # Determinar el nivel de alcohol y mostrarlo
    if valor_adc < 500:
        print("Aire limpio (sin alcohol):", valor_adc)
    elif valor_adc < 1500:
        print("Baja presencia de alcohol:", valor_adc)
    elif valor_adc < 3000:
        print("Concentración moderada:", valor_adc)
    else:
        print("Alta concentración de alcohol:", valor_adc)

    # Enviar dato a MQTT
    client.publish(MQTT_TOPIC, str(valor_adc))

    time.sleep(5)  # Esperar 10 segundos antes de la siguiente lectura
