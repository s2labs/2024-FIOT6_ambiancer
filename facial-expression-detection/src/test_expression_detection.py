from real_time_expression_detection import detect_expressions

if __name__ == '__main__':
    try:
        # Start the real-time facial expression detection with specified parameters.
        # Args:
        #     model (str): The model to use for expression detection. Default is 'vgg19'.
        #     debug_mode (bool): If True, displays the live video feed with expression annotations.
        #     buffer_size (int): The size of the buffer to average the expressions over.
        #     throttle_time (int): Minimum time between sending expressions to the MQTT broker.
        detect_expressions(model='vgg19', debug_mode=True, buffer_size=15, throttle_time=3)
    except KeyboardInterrupt:
        # Handle the KeyboardInterrupt exception to stop the detection gracefully.
        print("Interrupted by user, stopping detection...")