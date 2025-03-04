import machine
import time
import math
import network
from umqtt.simple import MQTTClient

# Configuración del pin analógico para leer la señal del sensor
adc = machine.ADC(machine.Pin(34))
adc.atten(machine.ADC.ATTN_0DB)
adc.width(machine.ADC.WIDTH_12BIT)

R1 = 10000

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/temp-kty024"

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

# Funciones para leer el voltaje y convertirlo a temperatura
def read_voltage():
    return (adc.read() / 4095) * 3.3

def voltage_to_temperature(voltage):
    R2 = R1 * (3.3 / voltage - 1)
    lnR2 = math.log(R2)
    return (1 / (0.001129148 + 0.000234125 * lnR2 + 0.0000000876741 * lnR2 ** 2)) - 273.15

while True:
    voltage = read_voltage()
    temperature = voltage_to_temperature(voltage)
    print("Voltaje: {:.2f} V - Temperatura: {:.2f} °C".format(voltage, temperature))
    
    # Publicar la temperatura en MQTT
    client.publish(MQTT_TOPIC, str(temperature))
    print(f"📡 Enviando temperatura: {temperature:.2f} °C")
    
    time.sleep(5)


