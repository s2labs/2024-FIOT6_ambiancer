import logging
import queue
import time
import paho.mqtt.client as mqtt

from constants import MQTT_BROKER_IP_ADDRESS, MQTT_TOPIC, MQTT_LOG_PATH
from utils import get_timestamp_string

# Setup logging to output MQTT events to a file
ts = get_timestamp_string()
log_filename = str(MQTT_LOG_PATH).replace('TIMESTAMP', ts)
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Thread-safe queue for sharing emotions
expression_queue = queue.Queue()

def on_connect(client, userdata, flags, reasonCode, properties=None):
    """
    Callback function for when the client receives a CONNACK response from the server.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata: The private user data as set in Client() or userdata_set().
        flags (dict): Response flags sent by the broker.
        reasonCode (int): The connection result.
        properties (mqtt.Properties, optional): MQTT v5.0 properties.
    """
    if reasonCode == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect to MQTT broker with code {reasonCode}")

def on_message(client, userdata, msg):
    """
    Callback function for when a PUBLISH message is received from the server.

    Args:
        client (mqtt.Client): The client instance for this callback.
        userdata: The private user data as set in Client() or userdata_set().
        msg (mqtt.MQTTMessage): An instance of MQTTMessage, which contains topic and payload.
    """
    logging.info(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")
    client.subscribe(msg.topic)

def start_mqtt():
    """
    Initializes and starts the MQTT client.

    Returns:
        mqtt.Client: The initialized and started MQTT client.
    """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_IP_ADDRESS)
    client.loop_start()
    return client

def stop_mqtt(client):
    """
    Stops the MQTT client.

    Args:
        client (mqtt.Client): The MQTT client to stop.
    """
    client.loop_stop()
    client.disconnect()

def mqtt_loop(stop_event=None):
    """
    Main loop for handling MQTT messages and publishing expressions from the queue.

    Args:
        stop_event (threading.Event, optional): An event to signal stopping the loop.
    """
    client = start_mqtt()
    try:
        while not stop_event.is_set():
            if not expression_queue.empty():
                expression = expression_queue.get()
                payload = expression.lower()
                client.publish(MQTT_TOPIC, payload)
                time.sleep(1)
    except KeyboardInterrupt:
        stop_mqtt(client)
    finally:
        stop_mqtt(client)