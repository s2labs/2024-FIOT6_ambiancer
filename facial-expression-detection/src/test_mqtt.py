import time
from mqtt_connection import start_mqtt, stop_mqtt
from constants import MQTT_TOPIC

if __name__ == '__main__':
    client = start_mqtt()
    try:
        while True:
            # Define the test expression to be published
            expression = 'TEST_EXPRESSION'
            # Convert the expression to lowercase to form the payload
            payload = expression.lower()
            # Publish the payload to the specified MQTT topic
            client.publish(MQTT_TOPIC, payload)
            # Wait for 1 second before publishing the next message
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the MQTT client gracefully on keyboard interrupt
        stop_mqtt(client)