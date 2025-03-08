import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-026"


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


# Configurar el pin del sensor táctil
sensor_pin = machine.Pin(13, machine.Pin.IN)  # Cambia el pin si es necesario

sensor_pinA = machine.Pin(34) 
adc = machine.ADC(sensor_pinA)  
adc.atten(machine.ADC.ATTN_0DB)  

# Bucle para leer el sensor
while True:
    valor_analogico = adc.read()  # Leer el valor analógico (0-4095)
    print("Valor analógico del sensor:", valor_analogico)
    
    if sensor_pin.value() == 1:
        print("Sensor táctil activado")
        client.publish(MQTT_TOPIC, str(valor_analogico))
    else:
        print("Sensor táctil desactivado")
    time.sleep(5)  # Pausa de 5 segundo entre lecturas



