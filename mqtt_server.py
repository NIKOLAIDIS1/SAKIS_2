import paho.mqtt.client as mqtt
import signal
import sys
import time
import threading

# MQTT Settings
BROKER = "mqtt.eclipseprojects.io"
PORT = 1883
USERNAME = "ersi"  # Replace with your actual username

# Topics
USER_ORDER_TOPIC = f"/MSIOT/{USERNAME}/USER_ORDER"  # Activate/Deactivate CONTROL BY USER  
ALARM_TOPIC = f"/MSIOT/{USERNAME}/ALARM"  # Alarm ON/OFF SENDING BY RASBEERY  ALARM SYSTEM 

# Global flag for running the program
running = True

# Store last message for each topic
last_messages = {USER_ORDER_TOPIC: None, ALARM_TOPIC: None}

#---------------------------------------------------------------------------------
def signal_handler(sig, frame):
    """Handles termination signals (e.g., Ctrl+C)."""
    global running
    print("\nSignal handler triggered! Terminating the program gracefully...", flush=True)
    running = False

def on_connect(client, userdata, flags, rc):
    """Callback for successful connection to the broker."""
    if rc == 0:
        print("\nSuccessfully connected to the MQTT broker.")
        print("Subscribing to topics:")
        print(f"  - User Order Topic: TRANSMITT BY USER  {USER_ORDER_TOPIC}")
        print(f"  - Alarm Topic  TRANSIMIT BY RASBERRY : {ALARM_TOPIC}")
        client.subscribe([(USER_ORDER_TOPIC, 0), (ALARM_TOPIC, 0)])
    else:
        print(f"Connection failed with error code: {rc}")

def on_message(client, userdata, msg):
    """Callback for when a message is received."""
    global last_messages
    last_messages[msg.topic] = msg.payload.decode('utf-8')
    print(f"Received message on topic '{msg.topic}': {last_messages[msg.topic]}\n")

    # Specific handling for USER_ORDER_TOPIC
    if msg.topic == USER_ORDER_TOPIC:
        print(f"Status update for {USER_ORDER_TOPIC}: {last_messages[msg.topic]}\n")

#----------------------------WHIC IS THE PURPOSE ---------------------------------------------------------

def terminate_program():
    """Simulates termination after 10 seconds for testing."""
    time.sleep(3)
    signal.raise_signal(signal.SIGINT)
#----------------------------------------------------------
def main():
    global running

    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(BROKER, PORT, 60)
        print("\nConnecting to the MQTT broker...")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        sys.exit(1)

    # Start MQTT loop in a separate thread
    client.loop_start()

    # Register signal handler for graceful termination
    signal.signal(signal.SIGINT, signal_handler)

    # Simulate termination after 10 seconds (for testing purposes)
    threading.Thread(target=terminate_program).start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    finally:
        # Stop MQTT loop and disconnect client
        print("Entering finally block...", flush=True)
        client.loop_stop()
        client.disconnect()

        # Print final status of topics
        print("\nFinal status of topics:", flush=True)
        for topic, message in last_messages.items():
            print(f"  - {topic}: {message}", flush=True)

        print("Disconnected from MQTT broker.", flush=True)

if __name__ == "__main__":
    main()
