import os
import time
import threading
import re


class LogHelper:
    def __init__(self, socketio, logger):
        self.socketio = socketio
        self.logger = logger
        self.log_dir = os.path.join(os.getcwd(), "logs")
        self.last_position = 0
        self.log_buffer = []  # Buffer to store recent logs
        self.max_buffer_size = 500  # Maximum number of log entries to keep in memory
        self.monitor_thread = None
        self.should_stop = False

        # Update regex pattern to better match your log format
        # This pattern handles both ROS formatted logs and direct output from programs
        self.ros_log_pattern = re.compile(r"\[(.*?)\] \[(.*?)\] \[(.*?)\]: (.*)")
        self.app_log_pattern = re.compile(r"\[(.*?)\] (.*)")

    def start_log_monitor(self):
        """Start the log monitoring thread"""
        if self.monitor_thread is None:
            self.should_stop = False
            self.monitor_thread = threading.Thread(
                target=self._monitor_logs, daemon=True
            )
            self.monitor_thread.start()
            self.logger.info("Log monitor thread started")

    def stop_log_monitor(self):
        """Stop the log monitoring thread"""
        if self.monitor_thread:
            self.should_stop = True
            self.monitor_thread.join(timeout=2.0)
            self.monitor_thread = None
            self.logger.info("Log monitor thread stopped")

    def get_recent_logs(self, count=100):
        """Return the most recent logs from the buffer"""
        return (
            self.log_buffer[-count:]
            if len(self.log_buffer) > count
            else self.log_buffer
        )

    def get_logs_from_file(self, count=100):
        """Read logs directly from the latest log file"""
        logs = []
        try:
            log_file = os.path.join(self.log_dir, "latest.log")
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    lines = f.readlines()
                    # Get the most recent lines, up to the requested count
                    recent_lines = lines[-count:] if len(lines) > count else lines

                    for line in recent_lines:
                        log_entry = self._parse_log_line(line)
                        if log_entry:
                            logs.append(log_entry)
        except Exception as e:
            self.logger.error(f"Error reading log file: {e}")

        return logs

    def _parse_log_line(self, line):
        """Parse a log line into a structured log entry"""
        try:
            # Several regex patterns to match different log formats

            # Format: [node.py-N] [LEVEL] [timestamp] [source]: message
            ros_format1 = re.match(
                r"\[([\w\.-]+)\] \[(INFO|ERROR|WARN|DEBUG)\] \[([\d\.]+)\] \[([\w\.]+)\]: (.*)",
                line,
            )

            # Format: [LEVEL] [node.py-N]: message
            ros_format2 = re.match(
                r"\[(INFO|ERROR|WARN|DEBUG|WARNING)\] \[([\w\.-]+)\]: (.*)", line
            )

            # Format: [node.py-N] message (like HTTP logs)
            app_format = re.match(r"\[([\w\.-]+)\] (.*)", line)

            # Handle ROS format with node first
            if ros_format1:
                node, level, timestamp, source, message = ros_format1.groups()
                timestamp_ms = int(float(timestamp) * 1000)  # Convert to milliseconds

            # Handle ROS format with level first
            elif ros_format2:
                level, node, message = ros_format2.groups()
                timestamp_ms = int(time.time() * 1000)  # Use current time

            # Handle simpler app format
            elif app_format:
                node, message = app_format.groups()
                level = "INFO"  # Default level

                # Try to determine level from message content
                if "error" in message.lower():
                    level = "ERROR"
                elif "warn" in message.lower():
                    level = "WARN"
                elif "debug" in message.lower():
                    level = "DEBUG"

                timestamp_ms = int(time.time() * 1000)  # Use current time

            # No pattern matched
            else:
                return {
                    "node": "unknown",
                    "timestamp": int(time.time() * 1000),
                    "level": "INFO",
                    "message": line.strip(),
                    "raw": line.strip(),
                }

            # Clean up node name - extract actual node name from patterns like [app.py-1]
            if "-" in node:
                # Extract base node name before the dash
                node = node.split("-")[0]

            # Remove .py if present
            if node.endswith(".py"):
                node = node[:-3]

            # Handle special cases like [launch]
            if node == "launch" or node == "ERROR" or node == "WARNING":
                node = "ros." + node

            return {
                "node": node,
                "timestamp": timestamp_ms,
                "level": level.upper(),  # Normalize level to uppercase
                "message": message.strip(),
                "raw": line.strip(),
            }

        except Exception as e:
            self.logger.error(f"Error parsing log line: {e}")
            return {
                "node": "unknown",
                "timestamp": int(time.time() * 1000),
                "level": "INFO",
                "message": f"Failed to parse: {line.strip()}",
                "raw": line.strip(),
            }

    def _monitor_logs(self):
        """Monitor the log file for changes and emit new lines via socketio"""
        latest_log_path = os.path.join(self.log_dir, "latest.log")
        self.last_position = 0

        while not self.should_stop:
            try:
                if os.path.exists(latest_log_path):
                    with open(latest_log_path, "r") as f:
                        # Seek to the last position we read
                        f.seek(self.last_position)

                        # Read new lines
                        new_lines = f.readlines()

                        if new_lines:
                            for line in new_lines:
                                log_entry = self._parse_log_line(line)
                                if log_entry:
                                    # Add to buffer
                                    self.log_buffer.append(log_entry)
                                    # Trim buffer if needed
                                    if len(self.log_buffer) > self.max_buffer_size:
                                        self.log_buffer = self.log_buffer[
                                            -self.max_buffer_size :
                                        ]

                                    # Emit to all connected clients
                                    self.socketio.emit("log_message", log_entry)

                        # Update the position for next time
                        self.last_position = f.tell()
            except Exception as e:
                self.logger.error(f"Error monitoring logs: {e}")

            # Sleep briefly before checking again
            time.sleep(0.5)

    def setup_socket_events(self):
        """Setup socket events for log-related functionality"""

        @self.socketio.on("request_logs")
        def handle_logs_request():
            try:
                # Get recent logs from our buffer
                logs = self.get_recent_logs(100)

                # Send each log entry
                for entry in logs:
                    self.socketio.emit("log_message", entry)

                # Only log at debug level since this is a routine operation
                self.logger.debug(f"Sent {len(logs)} log entries to client")
            except Exception as e:
                self.logger.error(f"Error handling log request: {e}")

        @self.socketio.on("clear_logs")
        def handle_clear_logs():
            # This only clears the client view, not the actual log files
            self.socketio.emit("logs_cleared")
            self.logger.debug("Client requested log view clearing")
