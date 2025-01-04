# Facial Expression Recognition for Ambiance Challenge

This repository (https://github.com/CiABAMBA/fiot6-hackathon.git) is the implementation of Facial Expression Recognition for the Ambiance challenge of the 6th edition of Future IoT PhD school.

## Module Composition

The module is composed of two main components:
1. **MQTT Connection**: Handles the communication with the MQTT broker.
2. **Facial Expression Recognition**: Detects and classifies facial expressions using either the VGG model (preferred) or the DeepFace library.

## Configuration

If needed, update the variables in `constants.py` to match your specific setup.

## Running the Complete Architecture

To run the complete architecture, execute the `run.py` script:
```bash
python ./src/run.py
```

### Command-line Arguments
- `model` (str): Model to use for emotion detection. Choose from 'vgg19' or 'deepface'. Default is 'vgg19'.
- `debug` (bool): Enable debug mode to show live video feed.
- `buffer_size` (int): Number of frames to average emotions over. Default is 15.
- `throttle_time` (int): Minimum seconds between sending expressions to the MQTT broker. Default is 5.

## Testing Individual Components
You can test individual using the test files:

### Test MQTT Connection
```bash
python ./src/test_mqtt_connection.py
```

### Test Facial Expression Recognition
```bash
python ./src/test_facial_expression_recognition.py
```

## Notes
- Both `run.py` and `test_mqtt.py` will fail and raise an exception if they cannot connect to an MQTT broker.
- The expression recognition can use the VGG model (preferred) or the DeepFace library.
- Uncomment `deepface` from `requirements.txt` if you want to use the DeepFace library.

## File Descriptions
- `constants.py`: Contains configuration constants such as file paths and MQTT settings.
- `run.py`: Main script to run the complete architecture.
- `test_expression_detection.py`: Script to test the facial expression detection component.
- `test_mqtt.py`: Script to test the MQTT connection component.
- `facial_expression_detection.py`: Contains the Detector class for facial expression detection.
- `mqtt_connection.py`: Handles MQTT connection and message publishing.
- `real_time_expression_detection.py`: Contains functions for real-time facial expression detection using a webcam.
- `utils.py`: Utility functions, including timestamp generation.
- `vgg.py`: Defines the VGG model architecture.
- `vgg_functions.py`: Functions to load the VGG model, preprocess images, and predict expressions.

## Dependencies
Ensure you have the following dependencies installed:  
- `torch`
- `torchvision`
- `opencv-python`
- `paho-mqtt`
- `numpy`
- `Pillow`
- `deepface` (optional, if using the DeepFace model)

Install the dependencies using pip:
```bash
pip install -r requirements.txt
```
