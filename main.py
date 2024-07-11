from dotenv import load_dotenv
import os
import json
import requests
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import logging.handlers
import os, sys
import time

load_dotenv()

# Get configuration from environment variables or use defaults
queue_filename = os.environ.get("QUEUE_FILENAME", "./payloads.json")
base_url = os.environ.get("API_BASE_URL", "https://thingsboard.url")
api_url = base_url + "/api/v1/{}/telemetry"
times = float(os.environ.get("TIME", 15))

if not os.path.exists(sys.path[0] + "/logs"):
    os.makedirs(sys.path[0] + "/logs")

# Set up logging
rotating_file_handler = logging.handlers.TimedRotatingFileHandler(
    filename='./logs/TB3DummyPayload.log',
    when="midnight",
    backupCount=7,
    utc=False,
    delay=True,
)

# Set handler name & format
stream_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[stream_handler, rotating_file_handler],
)

try:
    with open(queue_filename, "r") as f:
        queue_data = json.load(f)
except FileNotFoundError:
    logging.error(f"Queue file not found: {queue_filename}")
    queue_data = {}

def send_data_to_api(url, payload_data):
    try:
        response = requests.post(url, json=payload_data)
        response.raise_for_status()
        logging.info(f"Successfully sent data to {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to {url}: {e}")
        logging.error(f"Response status: {response.status_code}")
        logging.error(f"Response content: {response.text}")

def process_payload(payload_filename, device_tokens):
    # Construct the payload filename
    payload_filename = f"payloads/{payload_filename}.json"

    # Read the payload data from the corresponding file
    try:
        with open(payload_filename, "r") as f:
            payload_data = json.load(f)
    except FileNotFoundError:
        logging.error(f"Payload file not found: {payload_filename}")
        return

    # Send the POST request for each recipient token
    for device_token in device_tokens:
        send_data_to_api(api_url.format(device_token), {**payload_data, "sn": device_token})

def send_data():
    logging.info("Sending data to the API...")
    for payload_filename, device_tokens in queue_data.items():
        process_payload(payload_filename, device_tokens)
    logging.info("Data sending completed.")

def main():
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_data, "interval", minutes=times)
        scheduler.start()

        logging.info("Background scheduler started. Press Ctrl+C to stop.")
        while True:
            time.sleep(10000000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()