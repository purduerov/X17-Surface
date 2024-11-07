import signal
import time
import rclpy


class SignalHandler:

    def __init__(self, node):
        self.node = node
        self.shutdown = None


    def close_application(self, signal, frame):
        """
        Closing the application
        Triggered when the user presses Ctrl+C
        Camera streams are closed, SSH connection is closed, and the ROS node is destroyed
        """

        if self.shutdown:
            return
        self.shutdown = True

        try:
            if self.node is not None:
                self.node.get_logger().info("Closing application...")
                self.node.destroy_node()

            rclpy.shutdown()

        except Exception as e:
            if self.node is not None:
                self.node.get_logger().error("Error during shutdown: " + str(e))

        print("Application closed")
        exit(0)
