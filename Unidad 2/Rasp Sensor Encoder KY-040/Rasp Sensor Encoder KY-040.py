from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-040"


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




# Configuración de los pines
clk = Pin(14, Pin.IN, Pin.PULL_UP)  # Pin para CLK (Clock)
dt = Pin(12, Pin.IN, Pin.PULL_UP)  # Pin para DT (Data)
sw = Pin(13, Pin.IN, Pin.PULL_UP)  # Pin para el botón (SW)

# Variables globales para manejar la rotación
last_clk_state = clk.value()  # Último estado del pin CLK
counter = 0  # Contador de rotaciones

# Función para manejar la rotación
def rotar_encoder(pin):
    global last_clk_state, counter  # Declara las variables como globales
    clk_state = clk.value()
    dt_state = dt.value()

    if clk_state != last_clk_state:  # Detectar cambio de estado
        if dt_state != clk_state:  # Rotación en una dirección
            counter += 1
        else:  # Rotación en la otra dirección
            counter -= 1
        print("Contador:", counter)  # Imprime el valor del contador
        client.publish(MQTT_TOPIC, str(counter))

    last_clk_state = clk_state  # Actualizar el estado del CLK

# Detectar pulsación del botón
def verificar_boton(pin):
    if not sw.value():  # Si el botón está presionado (activo bajo)
        print("Botón presionado")

# Configurar interrupciones
clk.irq(trigger=Pin.IRQ_RISING, handler=rotar_encoder)  # Interrupción cuando CLK cambia de estado
sw.irq(trigger=Pin.IRQ_FALLING, handler=verificar_boton)  # Interrupción cuando el botón se presiona

# Mantener el programa corriendo para detectar las interrupciones
while True:
    time.sleep(0.1)  # Esperar un poco para evitar saturar el procesador
