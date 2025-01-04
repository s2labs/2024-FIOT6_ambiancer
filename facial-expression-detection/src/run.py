import argparse
import os
import threading

from mqtt_connection import mqtt_loop, stop_mqtt
from real_time_expression_detection import detect_expressions

def main():
    """
    Main function to start the real-time facial expression recognition with MQTT.

    Parses command-line arguments, sets up the environment, and starts the emotion detection
    and MQTT loop threads.

    Command-line arguments:
        --model (str): Model to use for emotion detection. Choose from 'vgg19' or 'deepface'.
        --debug (bool): Enable debug mode to show live video feed.
        --buffer_size (int): Number of frames to average emotions over.
        --throttle_time (int): Minimum seconds between sending expressions to the MQTT broker.
    """
    parser = argparse.ArgumentParser(description='Real-time Facial Expression Recognition with MQTT')
    parser.add_argument('--model', type=str, default='vgg19', help='Model to use for emotion detection. Choose from vgg19 or deepface')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode to show live video feed')
    parser.add_argument('--buffer_size', type=int, default=15, help='Buffer size to average emotions over')
    parser.add_argument('--throttle_time', type=int, default=5, help='Minimum seconds between sending expressions to the MQTT broker')
    args = parser.parse_args()

    # Check for DEBUG_MODE environment variable
    debug_mode = os.getenv('DEBUG_MODE', '0') == '1'
    if debug_mode:
        args.debug = True

    # Create a stop event
    stop_event = threading.Event()

    # Create and start the emotion detection thread
    emotion_thread = threading.Thread(target=detect_expressions, args=(args.model, args.debug, args.buffer_size, args.throttle_time, stop_event))
    emotion_thread.start()

    # Create and start the MQTT loop thread
    mqtt_thread = threading.Thread(target=mqtt_loop, args=(stop_event,))
    mqtt_thread.start()

    try:
        # Wait for both threads to finish
        emotion_thread.join()
        mqtt_thread.join()
    except KeyboardInterrupt:
        print("Interrupted by user, stopping threads...")
        stop_event.set()
        emotion_thread.join()
        mqtt_thread.join()

if __name__ == "__main__":
    main()