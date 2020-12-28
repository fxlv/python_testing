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
__version__ = "0.1"

import datetime
import os
import random
import signal
import sys
import time
import pytz
from collections import namedtuple

import paho.mqtt.client as mqtt

TIMEZONE="Europe/Riga"


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


StartTime = namedtuple("StartTime", "hour minute")
EndTime = namedtuple("EndTime", "hour minute")


def get_start_time(start_time: str) -> StartTime:
    start_time = start_time.split(":")
    s_time = StartTime(int(start_time[0]), int(start_time[1]))
    return s_time


def get_end_time(end_time: str) -> EndTime:
    end_time = end_time.split(":")
    e_time = EndTime(int(end_time[0]), int(end_time[1]))
    return e_time


def should_it_run(start_time: str, end_time: str) -> bool:
    """Return True if current time is > start_time and < end_time."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.datetime.now(tz)
    s_time = get_start_time(start_time)
    e_time = get_end_time(end_time)
    if now.hour >= s_time.hour and now.hour < e_time.hour:
        if now.hour > s_time.hour:
            # current hour is greater than start hour
            return True
        if now.hour == s_time.hour:
            # current hour is the same as start hour, need to check minute
            if now.minute >= s_time.minute:
                return True
        return False
    elif now.hour == e_time.hour:
        if now.minute < e_time.minute:
            return True
    return False


def handle_sigterm(sig, frame):
    raise SystemExit


if __name__ == "__main__":

    signal.signal(signal.SIGTERM, handle_sigterm)
    mqtt_server = os.getenv("MQTT_SERVER", None)
    mqtt_topic = os.getenv("MQTT_TOPIC", None)
    start_time = os.getenv("START_TIME", "12:00")
    end_time = os.getenv("END_TIME", "23:00")
    if mqtt_topic is None or mqtt_server is None:
        print("Please set MQTT_SERVER and MQTT_TOPIC environment variables.")
        sys.exit(1)
    mqtt_client = MqttClient(mqtt_server, mqtt_topic)
    try:
        while True:
            if should_it_run(start_time, end_time):
                main(mqtt_client)
            else:
                print("Not run time, sleeping.")
                time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("End of the line. Switching the light off.")
        mqtt_client.pub('{"state":"OFF"}')
