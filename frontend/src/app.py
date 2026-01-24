#!/usr/bin/env python3

# Standard imports
import os
import sys
import signal
import threading

# External imports
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv
import rclpy
from rclpy.node import Node

# Local imports
from utils.heartbeat_helper import HeartbeatHelper
from frontend_utils.frontend_handler import handle_frontend_event
from frontend_utils.log_helper import LogHelper
from frontend_utils.recording_api import RecordingRoutes  # Import the new module
from frontend_utils.controller_api import ControllerRoutes  # Import the new module


class Frontend(Node):
    def __init__(self):
        super().__init__("frontend")
        self.get_logger().info("Frontend node started")

        # Setup the heartbeat helper
        self.heartbeat_helper = HeartbeatHelper(self)

        # Setup the flask app
        self.app = Flask(__name__)
        CORS(self.app)
        # Add a secret key for the session
        self.app.secret_key = os.getenv("FLASK_SECRET_KEY", os.urandom(24).hex())
        self.socketio = SocketIO(self.app)
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

        # Setup the log helper
        self.log_helper = LogHelper(self.socketio, self.get_logger())

        # Get camera URLs from environment variables or use defaults
        self.camera_urls = {
            "camera1": os.getenv("CAMERA1_URL", "http://localhost:8889/camera_1"),
            "camera2": os.getenv("CAMERA2_URL", "http://localhost:8889/camera_2"),
            "camera3": os.getenv("CAMERA3_URL", "http://localhost:8889/camera_3"),
            "camera4": os.getenv("CAMERA4_URL", "http://localhost:8889/camera_4"),
        }

        self.get_logger().info(f"Camera URLs: {self.camera_urls}")

        ### ----- ROUTE SETUP ----- ###
        self.setup_routes()
        self.recording_routes = RecordingRoutes(self.app, self.get_logger())
        self.controller_routes = ControllerRoutes(self.app, self.get_logger())

        ### ----- SOCKETIO SETUP ----- ###
        self.setup_socketio_events()
        self.log_helper.setup_socket_events()

        ### ----- START SERVICES ----- ###
        # Start flask
        self.flask_thread = threading.Thread(target=self.run_flask)
        self.flask_thread.start()
        self.log_helper.start_log_monitor()  # Log helper

        # Setup publishers
        self.final_thrust_pub = None

    def run_flask(self):
        port = int(os.getenv("FLASK_PORT", 5013))
        self.socketio.run(
            self.app, host="0.0.0.0", port=port, allow_unsafe_werkzeug=True
        )

    # Function to setup the routes for the Flask app
    def setup_routes(self):
        # Default Route
        @self.app.route("/")
        def index():
            return redirect(url_for("home"), code=302)

        # Main UI
        @self.app.route("/home")
        def home():
            return render_template(
                "innovative_ui.html", active_page="home", camera_urls=self.camera_urls
            )

        ### -------- CAMERA PAGES -------- ###

        @self.app.route("/all-cameras")
        def all_cameras():
            return render_template(
                "all_cameras.html",
                active_page="all-cameras",
                camera_urls=self.camera_urls,
            )

        @self.app.route("/fullscreen-camera")
        def fullscreen_camera():
            camera = request.args.get(
                "camera", "1"
            )  # Default to camera 1 if not specified
            return render_template(
                "fullscreen_camera.html",
                active_page="fullscreen-camera",
                camera=camera,
                camera_urls=self.camera_urls,
            )

        ### -------- UTILITY PAGES -------- ###

        # The thrust testing page
        @self.app.route("/thruster-testing")
        def thrust_testing():
            return render_template(
                "thruster_testing.html", active_page="thruster-testing"
            )

        # Node status page
        @self.app.route("/node-status")
        def node_status():
            return render_template("node_status.html", active_page="node-status")

        # Logs page
        @self.app.route("/logs")
        def logs():
            return render_template("logs.html", active_page="logs")

        # Recordings page
        @self.app.route("/recordings")
        def recordings_page():
            return render_template("recordings.html", active_page="recordings")

        @self.app.route("/controller-mapping")
        def controller_mapping():
            return render_template(
                "controller_mapping.html", active_page="controller-mapping"
            )

    # Function to setup the socketio events
    def setup_socketio_events(self):
        @self.socketio.on("connect")
        def connect():
            # Only log first connection in a session, not reconnects
            if not hasattr(self, "_session_started"):
                self.get_logger().info("SocketIO client connected")
                self._session_started = True

        @self.socketio.on("disconnect")
        def disconnect():
            # Disconnects are expected during page navigation, so debug level is sufficient
            self.get_logger().debug("SocketIO client disconnected")

        # General-purpose event handler
        @self.socketio.on("*")  # Using '*' to catch all events
        def handle_all_events(event, data=None):
            # Handle frontend events
            if event.startswith("frontend-"):
                # Don't log high-frequency events like thruster values
                if not event.startswith("frontend-sendThrusterValues"):
                    self.get_logger().debug(f"Frontend event: {event}")
                # Handle the event
                handle_frontend_event(self, event, data)

            # Silently handle log-related events
            elif event.startswith("request_logs") or event.startswith("clear_logs"):
                pass

            # Forward all other events
            else:
                self.socketio.emit(event, data)


def main():
    rclpy.init()
    frontend = Frontend()

    # Silent exit on SIGINT - just terminate immediately
    def silent_exit(sig, frame):
        # Exit without any logging or cleanup
        frontend.log_helper.stop_log_monitor()
        os._exit(0)  # exit immediately without cleanup

    # Register the signal handler
    signal.signal(signal.SIGINT, silent_exit)
    signal.signal(signal.SIGTERM, silent_exit)

    try:
        rclpy.spin(frontend)
    except KeyboardInterrupt:
        # Exit silently on KeyboardInterrupt too
        os._exit(0)
    finally:
        # This will only run if spin() returns normally, not after os._exit()
        frontend.log_helper.stop_log_monitor()
        sys.exit(0)


if __name__ == "__main__":
    main()
