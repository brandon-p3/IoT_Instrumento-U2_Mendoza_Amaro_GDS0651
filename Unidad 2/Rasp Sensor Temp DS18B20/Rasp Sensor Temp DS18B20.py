import time
import machine
import onewire
import ds18x20
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/DS18B20"


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

# Configuración del sensor DS18B20
pin_sensor = machine.Pin(15)  # Prueba con GPIO4 si hay problemas
sensor = ds18x20.DS18X20(onewire.OneWire(pin_sensor))

# Buscar sensores en el bus 1-Wire
roms = sensor.scan()
if not roms:
    print("⚠ No se encontraron sensores DS18B20. Verifica la conexión.")
else:
    print("✅ Sensor detectado:", roms)

# Loop principal: Leer temperatura
try:
    while True:
        sensor.convert_temp()  # Iniciar medición
        time.sleep(1)  # Esperar la conversión

        for rom in roms:
            temp_c = sensor.read_temp(rom)  # Leer temperatura
            temp_str = "{:.2f}".format(temp_c)  # Formato correcto

            print("🌡 Temperatura:", temp_str, "°C")  # Mostrar en consola
            client.publish(MQTT_TOPIC, str(temp_str))
            

        time.sleep(5)  # Esperar 2 segundos antes de la siguiente medición

except Exception as e:
    print("❌ Error:", e)
