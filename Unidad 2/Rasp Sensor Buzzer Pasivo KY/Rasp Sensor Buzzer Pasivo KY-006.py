from machine import Pin, PWM
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi y MQTT
SSID = "GUS_LAP 9476"
PASSWORD = "@95X393b"
MQTT_BROKER = "192.168.137.144"
MQTT_TOPIC = "gds0651/actuator/KY-006"


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


# Definir el pin del buzzer pasivo
BUZZER_PIN = 15
buzzer = PWM(Pin(BUZZER_PIN))

# Definición de notas musicales (Frecuencias en Hz)
NOTES = {
    "B0": 31, "C1": 33, "CS1": 35, "D1": 37, "DS1": 39, "E1": 41,
    "F1": 44, "FS1": 46, "G1": 49, "GS1": 52, "A1": 55, "AS1": 58, "B1": 62,
    "C2": 65, "CS2": 69, "D2": 73, "DS2": 78, "E2": 82, "F2": 87, "FS2": 93,
    "G2": 98, "GS2": 104, "A2": 110, "AS2": 117, "B2": 123, "C3": 131,
    "CS3": 139, "D3": 147, "DS3": 156, "E3": 165, "F3": 175, "FS3": 185,
    "G3": 196, "GS3": 208, "A3": 220, "AS3": 233, "B3": 247, "C4": 262,
    "CS4": 277, "D4": 294, "DS4": 311, "E4": 330, "F4": 349, "FS4": 370,
    "G4": 392, "GS4": 415, "A4": 440, "AS4": 466, "B4": 494, "C5": 523,
    "CS5": 554, "D5": 587, "DS5": 622, "E5": 659, "F5": 698, "FS5": 740,
    "G5": 784, "GS5": 831, "A5": 880, "AS5": 932, "B5": 988, "C6": 1047,
    "CS6": 1109, "D6": 1175, "DS6": 1245, "E6": 1319, "F6": 1397, "FS6": 1480,
    "G6": 1568, "GS6": 1661, "A6": 1760, "AS6": 1865, "B6": 1976, "C7": 2093,
    "CS7": 2217, "D7": 2349, "DS7": 2489, "E7": 2637, "F7": 2794, "FS7": 2960,
    "G7": 3136, "GS7": 3322, "A7": 3520, "AS7": 3729, "B7": 3951, "C8": 4186,
    "CS8": 4435, "D8": 4699, "DS8": 4978, "REST": 0
}

# 🔹 Melodía: Imperial March (Star Wars)
imperial_march_melody = ["A4", "A4", "A4", "F4", "C5", "A4", "F4", "C5", "A4",
                          "E5", "E5", "E5", "F5", "C5", "GS4", "F4", "C5", "A4"]
imperial_march_durations = [350, 350, 350, 250, 100, 350, 250, 100, 700,
                            350, 350, 350, 250, 100, 350, 250, 100, 700]

# 🔹 Melodía: Super Mario Bros
mario_melody = ["E5", "E5", "REST", "E5", "REST", "C5", "E5",
                "G5", "REST", "G4", "REST",
                "C5", "REST", "G4", "REST", "E4",
                "REST", "A4", "B4", "AS4", "A4",
                "G4", "E5", "G5", "A5", "F5", "G5",
                "REST", "E5", "C5", "D5", "B4"]
mario_durations = [150, 150, 150, 150, 150, 150, 150,
                   150, 150, 150, 300,
                   150, 150, 150, 150, 150,
                   150, 150, 150, 150, 150,
                   150, 150, 150, 150, 150, 150,
                   150, 150, 150, 150, 150]

# 🔹 Melodía: Jingle Bells
jingle_bells_melody = ["E5", "E5", "E5", "E5", "E5", "E5",
                        "E5", "G5", "C5", "D5", "E5",
                        "F5", "F5", "F5", "F5",
                        "F5", "E5", "E5", "E5", "E5",
                        "E5", "D5", "D5", "E5",
                        "D5", "G5"]
jingle_bells_durations = [200, 200, 400, 200, 200, 400,
                          200, 200, 200, 200, 800,
                          200, 200, 200, 200,
                          200, 200, 200, 100, 100,
                          200, 200, 200, 200,
                          400, 400]

# Función para reproducir una nota
def play_tone(frequency, duration):
    if frequency == 0:
        time.sleep(duration / 1000)
    else:
        buzzer.freq(frequency)
        buzzer.duty(512)  # 50% ciclo de trabajo
        time.sleep(duration / 1000)
        buzzer.duty(0)  # Apagar buzzer
    time.sleep(0.05)  # Pausa entre notas

# Función para reproducir melodías
def play_melody(melody, durations, name):
    print("Reproduciendo:", name)
    for i in range(len(melody)):
        note = melody[i]
        duration = durations[i]
        frequency = NOTES.get(note, 0)
        play_tone(frequency, duration)

# Bucle principal para reproducir melodías en secuencia
while True:
    play_melody(imperial_march_melody, imperial_march_durations, "Imperial March")
    client.publish(MQTT_TOPIC, "1")
    time.sleep(5)

    play_melody(mario_melody, mario_durations, "Super Mario Bros")
    client.publish(MQTT_TOPIC, "2")
    time.sleep(5)

    play_melody(jingle_bells_melody, jingle_bells_durations, "Jingle Bells")
    client.publish(MQTT_TOPIC, "3")
    time.sleep(5)
