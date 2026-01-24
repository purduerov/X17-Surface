#!/usr/bin/env python3

# Import necessary libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from shared_msgs.msg import Bool
import socketio
import json

sio = socketio.Client()


class LeakSubscriberNode(Node):
    def __init__(self):
        super().__init__("leak_subscriber_node")
        self.topics = {"leak": self.rov_leak_callback}
        self.create_subscription(Bool, "leak_sensor", self.rov_leak_callback, 10)

    def rov_leak_callback(self, msg):
        msg_json = json.dumps({"leak_sensor": msg.data})
        sio.emit("leak_sensor", msg_json)


def main():
    rclpy.init()

    sio.connect("http://127.0.0.1:5000")

    leak_subscriber_node = LeakSubscriberNode()
    rclpy.spin(leak_subscriber_node)

    # Clean up after spinning finishes
    leak_subscriber_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
