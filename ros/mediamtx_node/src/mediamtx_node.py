#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from utils.heartbeat_helper import HeartbeatHelper
import socket
import os
import subprocess
import threading
import sys
import signal


# Create a publisher node that will publish a message counting up and down from 100 repeatedly
class MediaMTXNode(Node):
    def __init__(self):
        super().__init__("mediamtx_node")

        self.shutting_down = False

        # Setup heartbeat
        self.heartbeat_helper = HeartbeatHelper(self)

        # Create publisher to publish ip address to the topic /surface_ip
        self.publisher = self.create_publisher(String, "surface_ip", 10)
        self.timer = self.create_timer(1.0, self.publish_ip_address)
        self.ip_pub_count = 0
        self.ip_pub_count_max = 1000

        # Start the MediaMTX server process and monitor the process and watch for certain events and messages
        self.start_mediamtx_server()

    def publish_ip_address(self):
        msg = String()
        # Get the ip address of the surface computer
        ip = self.get_local_ip()
        self.get_logger().info(f"Publishing IP address: {ip}")
        msg.data = ip
        self.publisher.publish(msg)
        self.ip_pub_count += 1
        if self.ip_pub_count >= self.ip_pub_count_max:
            self.get_logger().info("Stopping publishing IP address")
            self.timer.cancel()

    def get_local_ip(self):
        try:
            # Create a socket and connect to a public server
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # Google's public DNS server
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception as e:
            return f"Error getting local IP: {e}"

    def start_mediamtx_server(self):
        def start_server():
            # Start the MediaMTX server process
            self.get_logger().info("Starting go2rtc server")
            # Ensure the executable is present before executing
            if os.path.exists("install/mediamtx_node/lib/mediamtx_node/go2rtc"):
                self.get_logger().info("go2rtc server executable found")
            else:
                self.get_logger().error("go2rtc server executable not found")
                return

            # Start the MediaMTX server process
            self.get_logger().info("Starting go2rtc server process")
            self.process = subprocess.Popen(
                [
                    "install/mediamtx_node/lib/mediamtx_node/go2rtc",
                    "-c install/mediamtx_node/lib/mediamtx_node/go2rtc.yaml",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            while True:
                if not self.shutting_down:
                    for line in self.process.stdout:
                        self.get_logger().info(line.strip())
                    for line in self.process.stderr:
                        self.get_logger().error(line.strip())
                    if self.process.poll() is not None:
                        self.get_logger().info("go2rtc server process has terminated")
                        break

        # Start the server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

    def cleanup(self):
        """Clean shutdown logic"""
        if self.shutting_down:
            return

        self.shutting_down = True

        # Kill the MediaMTX server process if it exists
        if hasattr(self, "process"):
            self.process.terminate()
            self.process.wait()


def main():
    rclpy.init()
    publisher_node = MediaMTXNode()

    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        publisher_node.cleanup()
        # Exit the program
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        rclpy.spin(publisher_node)
    except KeyboardInterrupt:
        # This should be caught by the signal handler, but just in case
        pass
    finally:
        # Clean up resources
        publisher_node.cleanup()
        sys.exit(0)


if __name__ == "__main__":
    main()
