#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect, url_for
from signal_handler import SignalHandler
import rclpy
import signal
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv(dotenv_path=f"/workspaces/X17-Surface/.env")


@app.route("/")
def index():
    return render_template("index.html", rov_ip=os.getenv("ROV_IP"))


def initialize_frontend_nodes():
    """
    Initializes the ROS node for the Flask server
    Returns the node object
    """
    rclpy.init()
    node = rclpy.create_node("flask_server")
    node.get_logger().info("Flask server started")
    return node


if __name__ == "__main__":
    """
    Main function for running the ROV
    To build the program, run `scripts/build.sh`
    To run the program, run `scripts/run.sh`
    """
    node = initialize_frontend_nodes()
    if node is None:
        print("ERROR: Could not initialize ROS node")
        exit(1)

    # Establish the signal handler for closing the application
    signal_handler = SignalHandler(node)
    signal.signal(signal.SIGINT, signal_handler.close_application)

    app.run(host="0.0.0.0", port=5000)
