from machine import ADC, Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "bgma/sensor/KY-039"


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



# Configuración del sensor KY-039 en el pin GPIO34
sensor_pulso = ADC(Pin(34))
sensor_pulso.atten(ADC.ATTN_11DB)  # Permite medir hasta 3.3V

# Configuración del LED indicador (Opcional, si el módulo tiene LED)
led_pin = Pin(13, Pin.OUT)  # Usa el GPIO13 o cámbialo según la conexión

# Variables para el cálculo de BPM
umbral = 2500  # Ajusta según el sensor y condiciones de luz
ultimo_pico = 0
contador_picos = 0
tiempo_inicio = time.ticks_ms()  # Tiempo inicial

print("Coloca tu dedo en el sensor...")

while True:
    valor = sensor_pulso.read()  # Leer sensor (0 - 4095)
    
    # Detectar picos (cuando el valor sobrepasa el umbral)
    if valor > umbral:
        if (time.ticks_ms() - ultimo_pico) > 300:  
            contador_picos += 1
            ultimo_pico = time.ticks_ms()
            led_pin.value(1)  # Enciende LED cuando detecta latido
    else:
        led_pin.value(0)  # Apaga LED cuando no hay latido

    # Calcular BPM cada 10 segundos
    if (time.ticks_ms() - tiempo_inicio) >= 10000:
        bpm = contador_picos * 6  # Escalar conteo de picos a 1 minuto
        print("Frecuencia Cardíaca (BPM):", bpm)
        client.publish(MQTT_TOPIC, str(bpm))

        # Reiniciar contador y tiempo de inicio
        contador_picos = 0
        tiempo_inicio = time.ticks_ms()

    print("Valor del sensor:", valor)  # Mostrar valores en consola
    time.sleep(1)  # Esperar antes de la siguiente lectura
