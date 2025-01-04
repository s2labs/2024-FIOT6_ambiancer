"""
Main logic to implement the final software

The behavior of the IR Clock is quite flaky as setting the time does not occur
as expected. Time can only be set in full minutes. For the mode of counting down,
the IR Blaster must send a "1" first, then "SET", and then the numbers. Although,
the behavior with time > 19 min and time < 10 min is quite difficult to handle.

It will be worth to try another clock, we only tried the "big" clock.
"""
import paho.mqtt.client as mqtt

from multiprocessing import Queue
from threading import Thread

import time

import matrix_ctrl

time_queue = Queue()
sentiment_queue = Queue()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

nums = {0: "0xFF9867",
        1: "0xFF30CF",
        2: "0xFF18E7",
        3: "0xFF7A85",
        4: "0xFF10EF",
        5: "0xFF38C7",
        6: "0xFF5AA5",
        7: "0xFF42BD",
        8: "0xFF4AB5",
        9: "0xFF52AD"}


def generate_string(data: str):
    "Generates the proper MQTT message for the Sonoff IR Blaster"
    return "{\"Protocol\":\"NEC\",\"Bits\": 32, \"data\":" + data + "}"


def send_msg(data: str):
    msg = generate_string(data)
    print(f"Sending... {data}")
    client.publish("cmnd/sonoff/IRsend", msg)


def do_sentiment():
    while True:
        data: str = sentiment_queue.get(True)
        matrix_ctrl.matrix_command(data.lower())
        time.sleep(5)


def do_time():
    while True:
        data = time_queue.get(True)
        data = data.split(":")
        send_msg("0xFF30CF")  # 1
        time.sleep(0.5)
        send_msg("0xFF02FD")  # SET
        time.sleep(0.5)
        for num in data:
            x = num[0]
            y = num[1]
            send_msg(nums[int(x)])
            time.sleep(0.5)
            send_msg(nums[int(y)])
            time.sleep(0.5)
            break
        send_msg("0xFFA857")  # OK


def mqtt_connect(client, userdata, flags, reason_code, properties):
    print("Connecting to topics...")
    client.subscribe("fiot/iot/time")
    client.subscribe("fiot/iot/mood")
    client.subscribe("fiot/iot/show")


def mqtt_message(client, userdata, msg):
    print(
        f"Received msg on {msg.topic} with {msg.payload.decode('utf-8')}")

    data = msg.payload.decode('utf-8')
    if "fiot/iot/time" in msg.topic:
        print("Putting time on display...")
        time_queue.put(data, True)
    else:
        sentiment_queue.put(data, True)


client.on_connect = mqtt_connect
client.on_message = mqtt_message

client.connect("192.168.2.53", 1883, 60)


thr_1 = Thread(target=do_time)
thr_1.start()
thr_2 = Thread(target=do_sentiment)
thr_2.start()
client.loop_forever()
