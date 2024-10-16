#!/usr/bin/env python3
import os
from flask import Flask, render_template, request, redirect, url_for
from ssh import Ssh
from streams import Streams
from signal_handler import SignalHandler
import rclpy
import signal



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def initialize_frontend_nodes():
    """
    Initializes the ROS node for the Flask server
    Returns the node object
    """
    rclpy.init()
    node = rclpy.create_node('flask_server')
    node.get_logger().info("Flask server started")
    return node


def establish_rov_connection(node):
    """
    Establishes a connection to the ROV
    Return the SSH client object
    """
    ssh = Ssh(node)
    rov_connection = ssh.connect()
    return rov_connection


def establish_camera_streams(node, rov_connection):
    """
    Starts the camera streams on the ROV
    """
    streams = Streams(node, rov_connection)
    streams.run_camera_streams() 
    return streams


if __name__ == '__main__':
    """ 
    Main function for running the ROV
    To build the program, run `scripts/build.sh`
    To run the program, run `scripts/run.sh`
    """
    node = initialize_frontend_nodes()
    if node is None:
        print("ERROR: Could not initialize ROS node")
        exit(1)

    rov_connection = establish_rov_connection(node)
    if rov_connection is None:
        node.get_logger().error("ERROR: Could not establish connection to ROV")
        exit(1)

    streams = establish_camera_streams(node, rov_connection)
    if streams is None:
        node.get_logger().error("ERROR: Could not start camera streams")
        exit(1)

    # Initialize SignalHandler with the created objects
    signal_handler = SignalHandler(node, rov_connection, streams)

    # Register the handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler.handler)

    app.run(host='0.0.0.0', port=5000)