from flask import Flask, request, jsonify, render_template_string, send_from_directory
import RPi.GPIO as GPIO
import json
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

LED_PIN = 17
STATE_FILE = 'state.json'
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Raspberry Pi LED Control</title>
    <style>
        .led-btn {
            border: none;
            background: none;
            cursor: pointer;
            outline: none;
        }
        img {
            width: 100px;
            height: 100px;
        }
    </style>
</head>
<body>
    <h1>Raspberry Pi LED Control</h1>
    <button class="led-btn" onclick="setLed('on')">
        <img src="/green_button.png" alt="Turn LED ON">
    </button>
    <button class="led-btn" onclick="setLed('off')">
        <img src="/red_button.png" alt="Turn LED OFF">
    </button>
    <p id="status"></p>
    <script>
        function setLed(state) {
            fetch('/led', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ state: state })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('status').innerText = data.status || data.error;
            })
            .catch(error => {
                document.getElementById('status').innerText = 'Error: ' + error;
            });
        }
    </script>
</body>
</html>
'''

def save_state(state):
    logging.debug(f"Saving state to {STATE_FILE}: {state}")
    with open(STATE_FILE, 'w') as f:
        json.dump({'state': state}, f)

def load_state():
    if not os.path.exists(STATE_FILE):
        logging.debug(f"{STATE_FILE} does not exist. Returning None.")
        return None
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
        logging.debug(f"Loaded state from {STATE_FILE}: {data.get('state')}")
        return data.get('state')

@app.route('/led', methods=['POST'])
def control_led():
    data = request.get_json()
    logging.info(f"Received POST /led with data: {data}")
    if not data or 'state' not in data:
        logging.warning("Missing 'state' in request data")
        return jsonify({'error': 'Missing state'}), 400
    requested_state = data['state'].lower()
    current_state = load_state()
    logging.info(f"Current state: {current_state}, Requested state: {requested_state}")
    if requested_state not in ['on', 'off']:
        logging.warning(f"Invalid state requested: {requested_state}")
        return jsonify({'error': 'Invalid state, use \"on\" or \"off\"'}), 400
    if requested_state == current_state:
        logging.info(f"LED already {requested_state}")
        return jsonify({'status': f'LED already {requested_state}'})
    if requested_state == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        logging.info("Set GPIO HIGH (LED ON)")
        save_state('on')
        return jsonify({'status': 'LED turned on'})
    elif requested_state == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        logging.info("Set GPIO LOW (LED OFF)")
        save_state('off')
        return jsonify({'status': 'LED turned off'})

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/green_button.png')
def green_button():
    return send_from_directory('.', 'green_button.png')

@app.route('/red_button.png')
def red_button():
    return send_from_directory('.', 'red_button.png')

if __name__ == '__main__':
    try:
        # Restore LED state from file on startup
        last_state = load_state()
        logging.info(f"Restoring LED state on startup: {last_state}")
        if last_state == 'on':
            GPIO.output(LED_PIN, GPIO.HIGH)
            logging.info("Set GPIO HIGH (LED ON) on startup")
        elif last_state == 'off':
            GPIO.output(LED_PIN, GPIO.LOW)
            logging.info("Set GPIO LOW (LED OFF) on startup")
        app.run(host='0.0.0.0', port=5000)
    finally:
        logging.info("Cleaning up GPIO on shutdown")
        GPIO.cleanup()

"""
Raspberry Pi LED Control API

This Flask app exposes an API to control an LED connected to GPIO 16 (BCM numbering) on a Raspberry Pi.

Pinout Relationship:
- GPIO 16 (BCM) corresponds to physical pin 36 on the Raspberry Pi header.
- To connect an LED:
    1. Connect the longer leg (anode, +) of the LED to GPIO 16 (physical pin 36) through a 220Ω resistor.
    2. Connect the shorter leg (cathode, -) of the LED to a ground pin (e.g., physical pin 34 or 39).

Testing High and Low Voltages:
- When the API sets GPIO 16 HIGH, the voltage between pin 36 (GPIO 16) and GND should be ~3.3V (LED ON).
- When the API sets GPIO 16 LOW, the voltage should be ~0V (LED OFF).
- You can test this with a multimeter:
    1. Place the black probe on a GND pin (e.g., pin 34 or 39).
    2. Place the red probe on pin 36 (GPIO 16).
    3. Use the API to toggle the LED and observe the voltage change.

Refer to the official Raspberry Pi pinout diagram for more details: https://pinout.xyz/
""" 