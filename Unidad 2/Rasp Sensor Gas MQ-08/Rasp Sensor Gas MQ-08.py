from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/MQ-08"


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


# Configurar el pin analógico donde está conectado el MQ-8
mq8 = ADC(Pin(34))  # GPIO34 (puedes cambiar el pin si lo deseas)
mq8.atten(ADC.ATTN_11DB)  # Rango de 0V a 3.3V

# Función para leer el valor del sensor MQ-8
def leer_gas():
    valor = mq8.read()  # Leer el valor analógico (0 - 4095)
    voltaje = valor * (3.3 / 4095)  # Convertir a voltaje

    
    umbral = 2000 

    # Imprimir valor y voltaje en consola
    print(f"Valor MQ-8: {valor} | Voltaje: {voltaje:.2f}V")

    if valor > umbral:
        print(f"¡Gas de hidrógeno detectado! Valor: {valor} | Voltaje: {voltaje:.2f}V")
        client.publish(MQTT_TOPIC, str(valor))

    return valor

# Bucle principal para leer el valor cada segundo
while True:
    leer_gas()
    time.sleep(1)  # Leer cada segundo
