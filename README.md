# Raspberry Pi LED Control API

This project provides a simple Flask API to control an onboard LED on a Raspberry Pi 1 using GPIO.

## Requirements
- Raspberry Pi OS
- Python 3
- Flask
- RPi.GPIO

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server (use sudo for GPIO access):
   ```bash
   sudo python3 app.py
   ```

## Usage
Send a POST request to control the LED (GPIO 16 by default):

- Turn LED ON:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"state": "on"}' http://<raspberrypi-ip>:5000/led
  ```
- Turn LED OFF:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"state": "off"}' http://<raspberrypi-ip>:5000/led
  ```

## Persistence
- The LED state is saved in a `state.json` file whenever it is changed via the API.
- On server startup, the last saved state is restored automatically.

## Notes
- Change `LED_PIN` in `app.py` if you want to use a different GPIO pin.
- Always run as root (sudo) to access GPIO. 