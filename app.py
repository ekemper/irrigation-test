from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

LED_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_json()
    if not data or 'state' not in data:
        return jsonify({'error': 'Missing state'}), 400
    state = data['state'].lower()
    if state == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        return jsonify({'status': 'LED turned on'})
    elif state == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        return jsonify({'status': 'LED turned off'})
    else:
        return jsonify({'error': 'Invalid state, use "on" or "off"'}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup() 