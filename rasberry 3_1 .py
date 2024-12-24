import paho.mqtt.client as mqtt
import signal
import threading
import sys
import time

# MQTT Settings
BROKER = "mqtt.eclipseprojects.io"
PORT = 1883
USERNAME = "ersi"  # Replace with your actual username

# Topics
USER_ORDER_TOPIC = f"/MSIOT/{USERNAME}/USER_ORDER"  # Activate/Deactivate CONTROL BY USER
ALARM_TOPIC = f"/MSIOT/{USERNAME}/ALARM"  # Alarm ON/OFF SENDING BY RASBERRY ALARM SYSTEM

# Global variables
detect_motion = False
is_night = False
user_order_active = False
running = True

# Signal handler for graceful termination
def signal_handler(sig, frame):
    global running
    print("\nSignal handler triggered! Terminating the program gracefully...")
    running = False

# Callback for successful connection to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nSuccessfully connected to the MQTT broker.")
        print("Subscribing to topics:")
        print(f"  - User Order Topic: {USER_ORDER_TOPIC}")
        client.subscribe(USER_ORDER_TOPIC)
        print(f"  - Alarm Topic: {ALARM_TOPIC}")
        client.subscribe(ALARM_TOPIC)
        print("Subscription to all topics successful!")
    else:
        print(f"Connection failed with error code: {rc}")

# Callback for when a message is received
def on_message(client, userdata, msg):
    global user_order_active
    if msg.topic == USER_ORDER_TOPIC:
        payload = msg.payload.decode("utf-8").strip().lower()
        print(f"Received command: {payload}")
        if payload == "user activate the alarm system":
            user_order_active = True
            print("USER_ORDER activated.")
        elif payload == "user deactivate the alarm system":
            user_order_active = False
            print("USER_ORDER deactivated.")

# Simulate sensor inputs and process alarm logic
def simulate_sensor_input(client):
    global detect_motion, is_night, user_order_active, running
    while running:
        try:
            user_input = input(
                "Enter '1' for motion detected, '0' for no motion, '2' for day, '3' for night, or 'exit' to quit: "
            )
            if user_input.lower() == "exit":
                running = False
                break

            if user_input == "1":
                detect_motion = True
                print("Motion detected.")
            elif user_input == "0":
                detect_motion = False
                print("No motion detected.")
            elif user_input == "2":
                is_night = False
                print("It is now daytime.")
            elif user_input == "3":
                is_night = True
                print("It is now nighttime.")
            else:
                print("Invalid input. Please try again.")

            # Debugging output
            print(f"Debug: user_order_active={user_order_active}, detect_motion={detect_motion}, is_night={is_night}")

            # Check conditions to activate the alarm
            if user_order_active and detect_motion and is_night:
                client.publish(ALARM_TOPIC, "ALARM !!!!!!!!", retain=False)
                print("Alarm activated!!!!!!")
            else:
                client.publish(ALARM_TOPIC, "Alarm deactivated. Stay calm.", retain=False)
                print("Alarm deactivated. Stay calm.")

        except KeyboardInterrupt:
            print("\nSensor input interrupted.")
            break

# Main function
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

    print("\nWaiting for messages from topics. You can now enter inputs after topics are initialized.")

    # Wait for a brief moment to ensure topics are subscribed
    time.sleep(1)

    # Start simulating sensor input after topics are initialized
    simulate_sensor_input(client)

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

    finally:
        # Stop MQTT loop and disconnect client
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker.")

if __name__ == "__main__":
    main()