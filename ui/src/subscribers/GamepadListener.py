#!/usr/bin/env python3

import json
import rclpy
from rclpy.node import Node
from shared_msgs.msg import RovVelocityCommand
from std_msgs.msg import Float64
import json


class GamepadSurfaceNode(Node):
    def __init__(self, window):
        super().__init__("surface_gamepad")
        self.subscription = self.create_subscription(
            RovVelocityCommand, "/rov_velocity", self.callback, 10
        )

        # Initialize the thrust array
        self.thrust = [0, 0, 0, 0, 0, 0, 0, 0]
        self.window = window
        print("initialized")

    def callback(self, data):
        #print('callback')
        fine = json.dumps(data.is_fine)
        pool_centric = json.dumps(data.is_pool_centric)
        pitch_lock = json.dumps(data.pitch_lock)
        depth_lock = json.dumps(data.pitch_lock)

        twist = data.twist
        linear = twist.linear

        self.window.ui.xoutput.display(linear.x)
        self.window.ui.youtput.display(linear.y)
        self.window.ui.zoutput.display(linear.z)
        self.window.ui.finemodeoutput.display(fine)

def main(args=None):
    rclpy.init(args=args)
    node = GamepadSurfaceNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
