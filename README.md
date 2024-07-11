# Dummy Payloads To Thingsboard

This is a Python script that sends dummy payload data to the ThingsBoard IoT platform. It reads the payload data from JSON files and sends them to the specified device tokens using the ThingsBoard REST API.

## Features

- Reads payload data from JSON files and sends them to the ThingsBoard platform
- Configurable API base URL, queue file, and time interval
- Logs all the actions to a rotating log file and the console
- Runs as a background task using the APScheduler library

## Prerequisites

- Python 3.7 or higher
- The following Python libraries:
  - `dotenv`
  - `requests`
  - `apscheduler`
  - `logging`

## Installation

1. Clone the repository:
```git clone https://github.com/your-username/Dummy-Payloads-To-Thingsboard.git```

2. Change to the project directory:
```cd Dummy-Payloads-To-Thingsboard```

3. Install the required Python packages:
```pip install -r requirements.txt```

4. Create a `.env` file in the project directory and set the following environment variables:
```QUEUE_FILENAME=./payloads.json API_BASE_URL=https://thingsboard.url TIME=15```

- `QUEUE_FILENAME`: The path to the JSON file containing the payload data and device tokens.
- `API_BASE_URL`: The base URL of the ThingsBoard API.
- `TIME`: The time interval in minutes for sending the payload data.

5. Create the `payloads` directory in the project directory to store the payload JSON files.

## Usage

1. Place your payload JSON files in the `payloads` directory. Each file should have a unique name and contain the payload data.

2. Run the script:
```python main.py```

The script will start a background task that sends the payload data to the specified device tokens every `TIME` minutes.

3. The script will log all the actions to the `./logs/TB3DummyPayload.log` file and the console.

## Customization

You can customize the following aspects of the script:

- `QUEUE_FILENAME`: The path to the JSON file containing the payload data and device tokens.
- `API_BASE_URL`: The base URL of the ThingsBoard API.
- `TIME`: The time interval in minutes for sending the payload data.
- Logging configuration: You can modify the logging settings, such as the log file name, log level, and log format.