# Exposing Your Flask App with ngrok

This guide will help you set up [ngrok](https://ngrok.com/) to expose your locally running Flask app (e.g., on a Raspberry Pi) to a public URL.

## 1. Install ngrok

- **On Raspberry Pi / Linux:**
  ```bash
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
  unzip ngrok-stable-linux-arm.zip
  sudo mv ngrok /usr/local/bin
  rm ngrok-stable-linux-arm.zip
  ```
- **On macOS:**
  ```bash
  brew install --cask ngrok
  ```
- **On Windows:**
  Download from [ngrok.com/download](https://ngrok.com/download) and unzip.

## 2. Sign Up and Authenticate

1. Go to [ngrok.com](https://ngrok.com/) and sign up for a free account.
2. After logging in, find your **Auth Token** on the dashboard.
3. Run the following command to add your auth token (replace `YOUR_AUTHTOKEN`):
   ```bash
   ngrok authtoken YOUR_AUTHTOKEN
   ```

## 3. Start Your Flask App

Make sure your Flask app is running on port 5000 (the default):
```bash
sudo python3 app.py
```

## 4. Start ngrok

In a new terminal, run:
```bash
ngrok http 5000
```

- This will create a public URL (e.g., `https://xxxx.ngrok.io`) that tunnels to your local Flask app.
- You will see the public URL in the terminal output.

## 5. Access Your App

- Open the public ngrok URL in your browser or share it with others.
- All requests to this URL will be forwarded to your local Flask app.

## 6. Tips
- The free ngrok plan gives you a random public URL each time you start it. Paid plans allow custom subdomains.
- Keep the ngrok terminal open while you want the tunnel to be active.
- For more options, see the [ngrok documentation](https://ngrok.com/docs). 