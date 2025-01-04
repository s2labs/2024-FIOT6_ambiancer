import threading
import time

import cv2
import numpy as np

from facial_expression_detection import Detector
from mqtt_connection import expression_queue

def setup_camera():
    """
    Sets up the camera for capturing video.

    Returns:
        cv2.VideoCapture: The video capture object.

    Raises:
        Exception: If the camera cannot be accessed.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Error: Could not access the camera.")
    return cap

def setup_cascade_classifier():
    """
    Sets up the Haar Cascade classifier for face detection.

    Returns:
        cv2.CascadeClassifier: The face cascade classifier.

    Raises:
        Exception: If the face cascade classifier cannot be loaded.
    """
    # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + str(HAARCASCADE_XML_PATH))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise Exception("Error: Could not load the face cascade classifier.")
    return face_cascade

def capture_frame(cap) -> np.ndarray:
    """
    Captures a frame from the video capture object.

    Args:
        cap (cv2.VideoCapture): The video capture object.

    Returns:
        np.ndarray: The captured video frame.

    Raises:
        Exception: If the video frame cannot be captured.
    """
    ret, frame = cap.read()
    if not ret:
        raise Exception("Error: Failed to capture video frame.")
    return frame

def get_frame_center(frame):
    """
    Gets the center coordinates of the video frame.

    Args:
        frame (np.ndarray): The video frame.

    Returns:
        tuple: The (x, y) coordinates of the frame center.
    """
    frame_height, frame_width = frame.shape[:2]
    return frame_width // 2, frame_height // 2

def detect_faces(frame, face_cascade):
    """
    Detects faces in the video frame using the Haar Cascade classifier.

    Args:
        frame (np.ndarray): The video frame.
        face_cascade (cv2.CascadeClassifier): The face cascade classifier.

    Returns:
        list: A list of detected faces, each represented by a (x, y, w, h) tuple.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def find_closest_to_center(faces, frame_center) -> tuple[int, int, int, int] | None:
    """
    Finds the face closest to the center of the frame.

    Args:
        faces (list): A list of detected faces, each represented by a (x, y, w, h) tuple.
        frame_center (tuple): The (x, y) coordinates of the frame center.

    Returns:
        tuple: The (x, y, w, h) tuple of the closest face.
    """
    closest_face = None
    min_distance = float('inf')
    for (x, y, w, h) in faces:
        face_center = (x + w // 2, y + h // 2)
        distance_to_center = np.sqrt((face_center[0] - frame_center[0]) ** 2 + (face_center[1] - frame_center[1]) ** 2)
        if distance_to_center < min_distance:
            min_distance = distance_to_center
            closest_face = (x, y, w, h)
    return closest_face

def crop_face(frame, face):
    """
    Crops the face region from the video frame.

    Args:
        frame (np.ndarray): The video frame.
        face (tuple): The (x, y, w, h) tuple representing the face region.

    Returns:
        np.ndarray: The cropped face region.
    """
    x, y, w, h = face
    return frame[y:y + h, x:x + w]

def annotate_frame(frame, face_xywh, expression):
    """
    Annotates the video frame with a rectangle around the face and the detected expression.

    Args:
        frame (np.ndarray): The video frame.
        face_xywh (tuple): The (x, y, w, h) tuple representing the face region.
        expression (str): The detected expression.
    """
    if face_xywh is not None:
        x, y, w, h = face_xywh
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, expression, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

def show_frame(frame):
    """
    Displays the video frame in a window.

    Args:
        frame (np.ndarray): The video frame.
    """
    cv2.imshow('Real-time Facial Expression Recognition', frame)

def get_dominant_expression(buffer) -> str | None:
    """
    Gets the dominant expression from the buffer.

    Args:
        buffer (list): A list of detected expressions.

    Returns:
        str | None: The dominant expression, or None if the buffer is empty.
    """
    if len(buffer) > 0:
        expression = max(set(buffer), key=buffer.count)
        print(expression, buffer)
        return expression
    return None

def update_buffer(buffer, expression, buffer_size):
    """
    Updates the buffer with the new expression.

    Args:
        buffer (list): The buffer of detected expressions.
        expression (str): The new detected expression.
        buffer_size (int): The maximum size of the buffer.

    Returns:
        list: The updated buffer.
    """
    if expression is not None:
        buffer.append(expression)
        if len(buffer) > buffer_size:
            buffer.pop(0)
    return buffer

def process_frame(frame, face_detector, expression_detector, return_face_xywh=False) -> tuple[str, tuple[int, int, int, int]] | str:
    """
    Processes the video frame to detect the closest face and its expression.

    Args:
        frame (np.ndarray): The video frame.
        face_detector (cv2.CascadeClassifier): The face cascade classifier.
        expression_detector (Detector): The expression detector.
        return_face_xywh (bool): Whether to return the face coordinates.

    Returns:
        tuple[str, tuple[int, int, int, int]] | str: The detected expression and face coordinates, or just the expression.
    """
    expression = None
    frame_center = get_frame_center(frame)
    faces = detect_faces(frame, face_detector)
    closest_face = find_closest_to_center(faces, frame_center)
    if closest_face is not None:
        face = crop_face(frame, closest_face)
        expression = expression_detector.detect(face)
    if return_face_xywh:
        return expression, closest_face
    return expression

def detect_expressions(model='vgg19', debug_mode=False, buffer_size=1, throttle_time=1, stop_event=None):
    """
    Detects expressions in real-time using the webcam.

    Args:
        model (str): The model to use for expression detection. Choose from 'vgg19' or 'deepface'.
        debug_mode (bool): If True, displays the live video feed with expression annotations.
        buffer_size (int): If > 1, uses a buffer to average the expressions over the last buffer_size frames.
        throttle_time (int): Minimum time between sending expressions to the MQTT broker.
        stop_event (threading.Event, optional): An event to signal stopping the loop.
    """
    face_detector = setup_cascade_classifier()
    expression_detector = Detector(model=model)
    capture = setup_camera()
    buffer = []
    last_sent_time = time.time()
    stop_event = stop_event or threading.Event()

    while not stop_event.is_set():
        try:
            frame = capture_frame(capture)
        except Exception as e:
            print(e)
            break

        expression, face_xywh = process_frame(frame, face_detector, expression_detector, return_face_xywh=True)
        update_buffer(buffer, expression, buffer_size)
        dominant_expression = get_dominant_expression(buffer)
        if dominant_expression:
            elapsed_time = time.time() - last_sent_time
            if elapsed_time >= throttle_time:
                expression_queue.put(dominant_expression)
                last_sent_time = time.time()
            expression_queue.put(dominant_expression)
        if debug_mode:
            annotate_frame(frame, face_xywh, dominant_expression)
            show_frame(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    if debug_mode:
        cv2.destroyAllWindows()