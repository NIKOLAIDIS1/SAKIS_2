# user can deactivate the alarm if it's enabled

import paho.mqtt.client as mqtt
import signal
import sys
import threading
import time

# MQTT Settings
BROKER = "mqtt.eclipseprojects.io"
PORT = 1883
USERNAME = "ersi"  # Replace with your actual username

# Topics
USER_ORDER_TOPIC = f"/MSIOT/{USERNAME}/USER_ORDER"  # Activate/Deactivate CONTROL BY USER  
ALARM_TOPIC = f"/MSIOT/{USERNAME}/ALARM"  # Alarm ON/OFF SENDING BY RASBEERY ALARM SYSTEM

# Global flag for running the program
running = True

# Store the last received alarm message
last_alarm_status = None

def signal_handler(sig, frame):
    """Handles termination signals."""
    global running
    print("\nSignal handler triggered! Terminating the program gracefully...")
    running = False

def on_connect(client, userdata, flags, rc):
    """Callback for successful connection to the broker."""
    if rc == 0:
        print("\nSuccessfully connected to the MQTT broker.")
        print("Subscribing to Alarm Topic:")
        print(f"  - Alarm Topic: {ALARM_TOPIC}")
        client.subscribe(ALARM_TOPIC)
    else:
        print(f"Connection failed with error code: {rc}")

def on_message(client, userdata, msg):
    """Callback for when a message is received."""
    global last_alarm_status
    if msg.topic == ALARM_TOPIC:
        last_alarm_status = msg.payload.decode('utf-8')
        print(f"Received alarm status BY RASPBERRY ALARM SYSTEM: {last_alarm_status}")

def handle_user_input(client):
    """Handles user input to publish to the USER_ORDER_TOPIC."""
    global running
    while running:
        try:
            user_input = input("Enter '1' to activate the ALARM SYSTEM, '0' to deactivate, or 'exit' to quit: ")

            if user_input.lower() == 'exit':
                print("Exiting user input thread.")
                running = False
                break

            if user_input == '1':
                client.publish(USER_ORDER_TOPIC, "user activate the alarm system", retain=True)
                print(f"Published 'ACTIVATE' to {USER_ORDER_TOPIC} with retain flag set.")
            elif user_input == '0':
                client.publish(USER_ORDER_TOPIC, "user deactivate the alarm system", retain=True)
                print(f"Published 'DEACTIVATE' to {USER_ORDER_TOPIC} with retain flag set.")
            else:
                print("Invalid input. Please enter '1', '0', or 'exit'.")
        except KeyboardInterrupt:
            print("\nUser input interrupted.")
            break

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

    # Start a thread for user input to send commands to the USER_ORDER_TOPIC
    threading.Thread(target=handle_user_input, args=(client,)).start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    finally:
        # Stop MQTT loop and disconnect client
        client.loop_stop()
        client.disconnect()

        # Print the last received alarm status
        print("\nFinal alarm status:")
        print(f"  - Alarm Topic: {last_alarm_status}")

        print("Disconnected from MQTT broker.")

if __name__ == "__main__":
    main()
