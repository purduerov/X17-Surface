#!/usr/bin/env python3

# Import necessary libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from shared_msgs.msg import RovVelocityCommand, ImuMsg
import socketio
import json

sio = socketio.Client()


# Create a subscriber node that will listen to multiple ROS topics
class SubscriberNode(Node):
    def __init__(self):
        super().__init__("subscriber_node")  # Initialize the node with a name

        # Dictionary to map topic names to their corresponding callback functions
        self.topics = {
            # 'count': self.count_callback,
            "rov_velocity": self.rov_velocity_callback,
            # Add more topics and their respective callbacks here
            "surface_imu": self.rov_imu_callback,
        }

        # Subscribe to each topic in the topics dictionary
        # self.create_subscription(String, 'count', self.count_callback, 10)
        self.create_subscription(
            RovVelocityCommand, "/rov_velocity", self.rov_velocity_callback, 10
        )
        self.create_subscription(ImuMsg, "/surface_imu", self.rov_imu_callback, 10)

    # def count_callback(self, msg):
    #     # General callback for all subscribed topics
    #     self.get_logger().info(f'Received from count topic: "{msg.data}"')
    #     # Emit the received message to the frontend using SocketIO
    #     sio.emit('count', msg.data)

    def rov_velocity_callback(self, msg):
        # First convert the ROS message to a dictionary
        msg_dict = rosmsg_to_dict(msg)
        # Then convert the dictionary to a JSON string
        msg_json = json.dumps(msg_dict)  # This ensures proper formatting
        # self.get_logger().info(f'Received from rov_velocity topic: "{msg}"')
        # Emit the received message to the frontend using SocketIO
        sio.emit("rov_velocity", msg_json)

    def rov_imu_callback(self, msg):
        msg_dict = rosmsg_to_dict(msg)

        msg_json = json.dumps(msg_dict)

        sio.emit("surface_imu", msg_json)


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
    subscriber_node = SubscriberNode()

    # Connect to the SocketIO server
    sio.connect("http://127.0.0.1:5000")  # Adjust the URL if necessary

    rclpy.spin(subscriber_node)
    subscriber_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
