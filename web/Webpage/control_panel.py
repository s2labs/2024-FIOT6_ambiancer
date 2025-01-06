from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as paho

app = Flask(__name__)

# MQTT Setup
# brokerPi = "192.168.2.53"
brokerPi = "127.0.0.1"
port = 1883
clientPi = paho.Client()
clientPi.connect(brokerPi, port)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    topic = data['topic']
    payload = data['payload']
    clientPi.publish(topic, payload)
    return jsonify({'status': 'Published successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
