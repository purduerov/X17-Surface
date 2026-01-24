#!/usr/bin/env python3

# Import necessary libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from shared_msgs.msg import TempMsg
import socketio
import json

sio = socketio.Client()


# Create a subscriber node that will listen to multiple ROS topics
class WaterTempSubscriber(Node):
    def __init__(self):
        super().__init__("water_temp_subscriber")

        # Dictionary to map topic names to their corresponding callback functions
        self.topics = {"water_temp": self.rov_water_temp_callback}

        # Subscribe to each topic in the topics dictionary
        self.create_subscription(
            Float32, "/water_temp", self.rov_water_temp_callback, 10
        )

    def rov_water_temp_callback(self, msg):
        msg_dict = rosmsg_to_dict(msg)
        msg_json = json.dumps(msg_dict)
        # self.get_logger().info(f'Received from water_temp topic: "{msg}"')
        sio.emit("water_temp", msg_json)


def rosmsg_to_dict(msg):
    """
    Convert any ROS message to a Python dictionary (recursive for nested messages).
    """
    msg_dict = {}

    if not hasattr(msg, "__slots__"):
        # If the attribute is not a ROS message (i.e., primitive or list), return its value
        return msg

    for field in msg.__slots__:  # Iterate over all fields in the message
        field_value = getattr(msg, field)

        # Remove leading underscore from the field name
        clean_field = field.lstrip("_")

        # If the field is a list of messages, process each item in the list
        if isinstance(field_value, list):
            msg_dict[clean_field] = [rosmsg_to_dict(item) for item in field_value]
        else:
            msg_dict[clean_field] = rosmsg_to_dict(
                field_value
            )  # Recurse for nested messages

    return msg_dict


def main():
    rclpy.init()
    water_temp_subscriber_node = WaterTempSubscriber()

    # Connect to the SocketIO server
    sio.connect("http://127.0.0.1:5000")  # Adjust the URL if necessary

    rclpy.spin(water_temp_subscriber_node)
    water_temp_subscriber_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
