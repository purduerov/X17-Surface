#!/usr/bin/env python3

# Import necessary libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Header
from shared_msgs.msg import RovVelocityCommand, FinalThrustMsg
import socketio
import json
import os
import signal
import sys
from dotenv import load_dotenv
from utils.heartbeat_helper import HeartbeatHelper

# Create a SocketIO client
sio = socketio.Client()


class UISubscriber(Node):
    def __init__(self):
        super().__init__("ui_subscriber")
        self.shutting_down = False

        # Setup the heartbeat helper
        self.heartbeat_helper = HeartbeatHelper(self)

        # Dictionary of topics to subscribe to and their message types
        self.topics = {
            # Frontend published topics
            "rov_velocity": RovVelocityCommand,
            "heartbeat": Header,
            # Core published topics
            "final_thrust": FinalThrustMsg,
        }

        # Subscribe to each topic in the topics dictionary
        for topic in self.topics:
            # self.get_logger().info(
            #     f"Subscribing to {topic} topic with message type {self.topics[topic].__name__}"
            # )
            self.create_subscription(
                self.topics[topic],
                topic,
                lambda msg, topic_name=topic: self.msg_callback(msg, topic_name),
                10,
            )

    def msg_callback(self, msg, topic_name):
        # Don't process messages if we're shutting down
        if self.shutting_down:
            return

        # Ignore the heartbeat message
        if topic_name == "heartbeat":
            return
        # Log the received message
        # self.get_logger().info(f'Received from {topic_name} topic: "{msg}"')
        # Convert the ROS message to JSON
        msg_dict = rosmsg_to_dict(msg)
        # Log the dict
        msg_json = json.dumps(msg_dict)
        # Emit the received message to the frontend using SocketIO
        if sio.connected:
            sio.emit(topic_name, msg_json)

    def cleanup(self):
        """Clean shutdown logic"""
        if self.shutting_down:
            return

        self.shutting_down = True

        # Disconnect from SocketIO server
        if sio.connected:
            try:
                sio.disconnect()
            except Exception as e:
                pass


def rosmsg_to_dict(msg):
    """
    Convert any ROS message to a Python dictionary (recursive for nested messages).
    """

    # If it looks like a numpy array, convert it to a list
    if hasattr(msg, "dtype") and hasattr(msg, "tolist"):
        return msg.tolist()

    # If it's not a ROS message, return it as-is
    if not hasattr(msg, "__slots__"):
        return msg

    msg_dict = {}
    for field in msg.__slots__:
        field_value = getattr(msg, field)
        clean_field = field.lstrip("_")

        # Handle lists of items
        if isinstance(field_value, list):
            msg_dict[clean_field] = [rosmsg_to_dict(item) for item in field_value]
        else:
            msg_dict[clean_field] = rosmsg_to_dict(field_value)

    return msg_dict


def main():
    rclpy.init()
    ui_subscriber = UISubscriber()

    # Connect to the SocketIO server
    load_dotenv(dotenv_path=f"/workspaces/X17-Surface/.env")
    port = str(os.getenv("FLASK_PORT", 5013))

    try:
        sio.connect("http://127.0.0.1:" + port)
        ui_subscriber.get_logger().info(f"Connected to SocketIO server at port {port}")
    except Exception as e:
        ui_subscriber.get_logger().error(f"Failed to connect to SocketIO server: {e}")

    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        ui_subscriber.cleanup()
        # Exit the program
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        rclpy.spin(ui_subscriber)
    except KeyboardInterrupt:
        # This should be caught by the signal handler, but just in case
        pass
    finally:
        # Clean up resources
        ui_subscriber.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    main()
