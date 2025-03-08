from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "mnml/sensor/KY-023"


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

# Definir los pines para los ejes X y Y del joystick (usando entradas analógicas)
x_analog = ADC(Pin(34))  # Pin para el eje X
y_analog = ADC(Pin(35))  # Pin para el eje Y

# Configurar el rango de los valores analógicos (por defecto 0-1023 en la mayoría de los microcontroladores)
x_analog.atten(ADC.ATTN_0DB)  # Configurar para lectura de 0-3.3V
y_analog.atten(ADC.ATTN_0DB)

# Definir umbrales para identificar el movimiento
LEFT_THRESHOLD = 400
RIGHT_THRESHOLD = 600
UP_THRESHOLD = 400
DOWN_THRESHOLD = 600

print("Esperando movimientos y presionar el botón del joystick...")

while True:
    # Leer los valores analógicos de los ejes X y Y
    x_value = x_analog.read()  # Leer valor X (0-1023)
    y_value = y_analog.read()  # Leer valor Y (0-1023)
    
    # Determinar dirección del movimiento
    if x_value < LEFT_THRESHOLD:
        horizontal = "Izquierda"
    elif x_value > RIGHT_THRESHOLD:
        horizontal = "Derecha"
    else:
        horizontal = "Centro"

    if y_value < UP_THRESHOLD:
        vertical = "Arriba"
    elif y_value > DOWN_THRESHOLD:
        vertical = "Abajo"
    else:
        vertical = "Centro"
    
    total = x_value + y_value
    # Imprimir la dirección
    print(f"Movimiento Horizontal: {horizontal}, Movimiento Vertical: {vertical}")
    client.publish(MQTT_TOPIC, str(total))
    
    time.sleep(5)  # Espera un poco antes de volver a leer los valores
