import time
import json
import random
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
TOPIC = "weather/station1"

client = mqtt.Client()


def connect():
    print(f"Connecting to MQTT broker {BROKER} ...")
    client.connect(BROKER, 1883, 60)


def publish_weather():
    while True:
        temperature = round(random.uniform(10, 25), 2)
        humidity = round(random.uniform(40, 70), 2)

        data = {
            "temperature": temperature,
            "humidity": humidity
        }

        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")

        time.sleep(3)


if __name__ == "__main__":
    connect()
    publish_weather()