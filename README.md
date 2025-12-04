## Table of Contents
- [SwooshFile](#swooshfile)
  - [Features](#features)
  - [Manual Installation](#manual-installation)
  - [Docker](#docker)
  - [Usage](#usage)
  - [Tested Environment](#tested-environment)

# SwooshFile

SwooshFile is a simple web-browser-based local network file-sharing service that enables seamless file sharing between devices. It works across multiple platforms, including macOS, Linux, Windows, Android, iOS, and more. No additional software is required—just a browser!

## Features
- Peer-to-peer local network file sharing.
- No account or registration needed.
- Cross-platform compatibility.
- User-friendly web-based interface.
- Secure and fast transfers.

## Manual Installation

**SwooshFile, for now, has to be self-hosted. Follow the steps below to set up your own instance:**

1. Clone the repository:
   ```
   git clone https://github.com/kijimoshi1337/SwooshFile.git
   ```

2. Navigate to the project directory:
   ```
   cd SwooshFile
   ```

3. Create enviroment:
   ```
   python3 -m venv venv
   ```

4. Activate enviroment:
   ```
   source venv/bin/activate
   ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Start the server:
   ```
   python3 app.py
   ```

## Docker

To build a docker container image use:
```
docker build -t swooshfile:latest .
```

Then start the container:
```
sudo docker run --name swooshfile -d -p 80:80 -v /app/uploads/:/app/uploads/:z --restart unless-stopped swooshfile:latest
```

## Usage

1. Open your browser and navigate to `http://localhost` to start sharing files.

2. To access files from another device check ip address of the host device and navigate to `http://<your ip>`

## Tested Environment
This application has been tested on the following platforms:
- Windows 10 & 11
- macOS Tahoe
- Ubuntu 22.04
- Android 15 (Chrome, Firefox)
- iOS 26.1 (Safari, Chrome)

## Support the Project ☕️
If you find SwooshFile useful and would like to support its development, consider buying me a coffee!

[PayPal](https://www.paypal.me/kijimoshi05)
