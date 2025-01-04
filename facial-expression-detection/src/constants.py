from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Model constants
WEIGHTS_PATH = PROJECT_ROOT / 'data/model_weights/FER2013_VGG19.t7'
HAARCASCADE_XML_PATH = PROJECT_ROOT / 'haarcascade_frontalface_default.xml'
EXPRESSIONS_LOG_PATH = PROJECT_ROOT / 'logs/expressions_log_TIMESTAMP.txt'
CLASS_NAMES = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# MQTT constants
MQTT_BROKER_IP_ADDRESS = "192.168.2.53"
MQTT_TOPIC = "fiot/iot/mood"
MQTT_LOG_PATH = PROJECT_ROOT / 'logs/mqtt_log_TIMESTAMP.txt'