#!/usr/bin/env python
#
# I bought an IKEA Tradfri color bulb and needed to make an xmas
# decoration using it.
#
# This script is used to control the bulb by setting random brightness and colour.
# Bulb is connected to a zigbee2mqtt bridge.
# The script sends command by publishing them to the relevant MQTT topic.
#
#
#
import os
import random
import time
import paho.mqtt.client as mqtt
import sys


class MqttClient():
    def __init__(self, server, topic):
        self.server = server
        self.topic = topic
        self.connect_to_mqtt()

    def connect_to_mqtt(self):
        self.client = mqtt.Client("Python light script")
        self.client.connect(self.server)

    def pub(self, payload):
        self.client.publish(self.topic, payload)


def rand_brightness():
    return random.choice(range(10, 250))


def rand_sleep():
    sleep_time = random.choice(range(10, 50))
    sleep_time = sleep_time / 10
    time.sleep(sleep_time)
    print(f"Sleeping for {sleep_time}")


def rand_x():
    x = random.choice(range(1, 10))
    x = x / 10
    return x


def rand_y():
    y = random.choice(range(1, 10))
    y = y / 10
    return y


def main(mqtt_client):
    x = 0.0
    y = 0.1
    brightness = 10

    for i in range(1, 10):
        x = x + 0.1
        brightness = rand_brightness()
        msg = f"""{{"state":"ON","brightness":{brightness}, "color":{{"x":{x}, "y":{y} }} }}"""
        mqtt_client.pub(msg)
        print(msg)
        rand_sleep()

    x = 0.0
    for i in range(1, 10):
        y = y + 0.1
        brightness = rand_brightness()
        msg = f"""{{"state":"ON","brightness":{brightness}, "color":{{"x":{x}, "y":{y} }} }}"""
        mqtt_client.pub(msg)
        print(msg)
        rand_sleep()

    for i in range(1, 100):
        x = rand_x()
        y = rand_y()
        brightness = rand_brightness()
        msg = f"""{{"state":"ON","brightness":{brightness}, "color":{{"x":{x}, "y":{y} }} }}"""
        mqtt_client.pub(msg)
        print(msg)
        rand_sleep()


if __name__ == "__main__":
    mqtt_server = os.getenv("MQTT_SERVER", None)
    mqtt_topic = os.getenv("MQTT_TOPIC", None)
    if mqtt_topic is None or mqtt_server is None:
        print("Please set MQTT_SERVER and MQTT_TOPIC environment variables.")
        sys.exit(1)
    mqtt_client = MqttClient(mqtt_server, mqtt_topic)
    try:
        while True:
            main(mqtt_client)
    except KeyboardInterrupt:
        print("End of the line. Switching the light off.")
        mqtt_client.pub('{"state":"OFF"}')
