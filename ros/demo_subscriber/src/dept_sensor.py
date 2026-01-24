#!/usr/bin/env python3

# Import necessary libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from shared_msgs.msg import RovVelocityCommand, ImuMsg, Float64
import socketio
import json

sio = socketio.Client()


class DepthSubscriberNode(Node):
    def __init__(self):
        super().__init__("depth_subscriber_node")
        self.topics = {"depth": self.rov_depth_callback}
        self.create_subscription(Float64, "depth", self.rov_depth_callback, 10)

    def rov_depth_callback(self, msg):
        msg_json = json.dumps({"depth": msg.data})
        sio.emit("depth", msg_json)


def main():
    rclpy.init()

    sio.connect("http://127.0.0.1:5000")

    depth_subscriber_node = DepthSubscriberNode()
    rclpy.spin(depth_subscriber_node)

    # Clean up after spinning finishes
    depth_subscriber_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
