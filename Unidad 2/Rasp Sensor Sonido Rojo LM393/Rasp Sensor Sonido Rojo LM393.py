import time
import network
from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient

SENSOR_PIN_DO = 12
SENSOR_PIN_AO = 34
BUZZER_PIN = 27  
THRESHOLD = 800  # Ajusta el umbral según la prueba

sensor_do = Pin(SENSOR_PIN_DO, Pin.IN)
sensor_ao = ADC(Pin(SENSOR_PIN_AO))
sensor_ao.atten(ADC.ATTN_0DB)

buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty(0)

mqtt_broker = "192.168.137.144"
mqtt_port = 1883
mqtt_topic = "mnml/sensor/sonido-LM393"
mqtt_client_id = "sound_sensor_{}".format(int(time.time()))

wifi_ssid = "GUS_LAP 9476"
wifi_password = "@95X393b"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_ssid, wifi_password)

    for _ in range(10):
        if wlan.isconnected():
            print('Wi-Fi conectado:', wlan.ifconfig())
            return True
        time.sleep(1)

    print("Error: No se pudo conectar a Wi-Fi")
    return False

def connect_mqtt():
    try:
        client = MQTTClient(mqtt_client_id, mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado a MQTT")
        return client
    except Exception as e:
        print("Error MQTT:", e)
        return None

def beep(duration=0.5, frequency=2000):
    buzzer.freq(frequency)
    buzzer.duty(512)  
    time.sleep(duration)
    buzzer.duty(0)  

def publish_data(client):
    if not client:
        return

    sound_detected = sensor_do.value()
    sound_intensity = sensor_ao.read()

    if sound_intensity > THRESHOLD or sound_detected:
        payload = "⚠️ Sonido fuerte detectado! Intensidad: {}".format(sound_intensity)
        mensajeF = "{}".format(sound_intensity)
        client.publish(mqtt_topic, mensajeF)
        print("🔊 Enviado:", payload)
        beep()

if connect_wifi():
    client = connect_mqtt()

    while True:
        publish_data(client)
        time.sleep(1)
else:
    print("No se pudo conectar a Wi-Fi.")
