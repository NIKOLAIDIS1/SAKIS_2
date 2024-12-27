Description of the MQTT Alarm System
Overview:

This system is designed to manage an alarm system using MQTT protocol for communication. It integrates a user interface, a central MQTT broker, and a Raspberry Pi-based alarm system that responds to sensor inputs and user commands.
Components:

    User Client:
        Functionality:
            Allows the user to control the alarm system by sending commands (activate or deactivate).
            Monitors the alarm status by subscribing to relevant updates.
        Key Operations:
            Publishes commands to the USER_ORDER topic.
            Subscribes to the ALARM topic to receive the current status.
        Example Commands:
            "Activate the alarm system."
            "Deactivate the alarm system."

    Raspberry Alarm System:
        Functionality:
            Simulates sensors (e.g., motion detection and day/night status).
            Processes user commands to activate or deactivate the alarm.
            Sends alarm status based on conditions.
        Key Operations:
            Subscribes to the USER_ORDER topic to receive user commands.
            Publishes alarm status to the ALARM topic.
        Alarm Logic:
            The alarm activates if:
                Motion is detected.
                It's nighttime.
                The user has activated the system.
            Otherwise, the alarm remains off.

    MQTT Broker:
        Functionality:
            Acts as the communication hub.
            Routes messages between the user client and the Raspberry Alarm System.
        Topics:
            USER_ORDER: For user commands.
            ALARM: For alarm status updates.

    Server/Monitor:
        Functionality:
            Displays real-time updates on the status of the alarm system.
            Subscribes to the ALARM topic for receiving updates.

Workflow:

    User Input:
        The user interacts with the User Client to send commands.
        Example: Activating the alarm system by sending a command to the USER_ORDER topic.

    Command Processing:
        The Raspberry Alarm System receives the user command.
        Simulated sensors determine if motion is detected and whether it's nighttime.

    Alarm Activation:
        The Raspberry Alarm System evaluates:
            Sensor inputs.
            User activation command.
        If conditions are met, it publishes an alarm activation message to the ALARM topic.

    System Updates:
        The User Client and Server/Monitor receive updates on the ALARM topic.
        Example: Displaying the alarm status to the user.

Topics and Communication:

    USER_ORDER:
        Used by the User Client to send activation or deactivation commands.
        Subscribed to by the Raspberry Alarm System.
    ALARM:
        Used by the Raspberry Alarm System to send status updates (e.g., Alarm activated or deactivated).
        Subscribed to by the User Client and Server/Monitor.

This setup enables seamless interaction between the user and the alarm system while ensuring real-time status updates.

