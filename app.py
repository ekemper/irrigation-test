from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import json
import os

app = Flask(__name__)

LED_PIN = 16
STATE_FILE = 'state.json'
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump({'state': state}, f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
        return data.get('state')

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_json()
    if not data or 'state' not in data:
        return jsonify({'error': 'Missing state'}), 400
    requested_state = data['state'].lower()
    current_state = load_state()
    if requested_state not in ['on', 'off']:
        return jsonify({'error': 'Invalid state, use "on" or "off"'}), 400
    if requested_state == current_state:
        return jsonify({'status': f'LED already {requested_state}'})
    if requested_state == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        save_state('on')
        return jsonify({'status': 'LED turned on'})
    elif requested_state == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        save_state('off')
        return jsonify({'status': 'LED turned off'})

if __name__ == '__main__':
    try:
        # Restore LED state from file on startup
        last_state = load_state()
        if last_state == 'on':
            GPIO.output(LED_PIN, GPIO.HIGH)
        elif last_state == 'off':
            GPIO.output(LED_PIN, GPIO.LOW)
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup() 