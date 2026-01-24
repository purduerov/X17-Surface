import os
import glob
import re
import subprocess
from datetime import datetime
from flask import jsonify, request, send_file, abort, render_template


class RecordingRoutes:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger
        self.register_routes()

    def register_routes(self):
        """Register all recording-related routes with the Flask app"""

        @self.app.route("/api/record/start/<camera_number>", methods=["POST"])
        def start_recording(camera_number):
            try:
                # Validate camera number
                if camera_number not in ["1", "2", "3", "4"]:
                    return jsonify(
                        {"success": False, "message": "Invalid camera number"}
                    )

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                videos_dir = os.path.join(os.getcwd(), "videos")
                output_path = os.path.join(
                    videos_dir, f"camera_{camera_number}_{timestamp}.mp4"
                )
                stream_url = f"rtsp://localhost:8554/camera_{camera_number}"

                # Ensure the videos directory exists
                os.makedirs(videos_dir, exist_ok=True)

                # Use ffmpeg to start recording the stream
                command = f"ffmpeg -i {stream_url} -c copy {output_path}"
                os.system(f"nohup {command} &")

                return jsonify({"success": True})

            except Exception as e:
                return jsonify({"success": False, "message": str(e)})

        @self.app.route("/api/record/stop/<camera_number>", methods=["POST"])
        def stop_recording(camera_number):
            try:
                # Validate camera number
                if camera_number not in ["1", "2", "3", "4"]:
                    return jsonify(
                        {"success": False, "message": "Invalid camera number"}
                    )

                # Find the ffmpeg process and kill it
                stream_url = f"rtsp://localhost:8554/camera_{camera_number}"
                command = f"pkill -f 'ffmpeg -i {stream_url}'"
                os.system(command)

                return jsonify({"success": True})

            except Exception as e:
                return jsonify({"success": False, "message": str(e)})

        @self.app.route("/api/recordings")
        def get_recordings():
            # Get all MP4 files in the videos directory using absolute path
            videos_dir = os.path.join(os.getcwd(), "videos")
            mp4_files = glob.glob(os.path.join(videos_dir, "*.mp4"))

            # Create a list of recording objects with metadata
            recordings = []
            for file in mp4_files:
                # Parse the filename to get camera and timestamp
                filename = os.path.basename(file)

                # Get file creation time
                creation_time = os.path.getctime(file)

                # Get video duration using ffprobe
                duration = "00:00"
                try:
                    result = subprocess.run(
                        [
                            "ffprobe",
                            "-v",
                            "error",
                            "-show_entries",
                            "format=duration",
                            "-of",
                            "default=noprint_wrappers=1:nokey=1",
                            file,
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )

                    if result.stdout:
                        # Convert seconds to MM:SS format
                        seconds = float(result.stdout)
                        minutes = int(seconds // 60)
                        seconds = int(seconds % 60)
                        duration = f"{minutes:02d}:{seconds:02d}"
                except Exception as e:
                    self.logger.error(f"Error getting video duration: {str(e)}")

                # Extract date from filename
                date_match = re.search(
                    r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})", filename
                )
                date = (
                    date_match.group(1)
                    if date_match
                    else datetime.fromtimestamp(creation_time).strftime(
                        "%Y-%m-%d_%H-%M-%S"
                    )
                )

                recordings.append(
                    {
                        "id": filename,  # Use filename directly as ID
                        "filename": filename,
                        "date": date,
                        "creation_time": creation_time,
                        "size": os.path.getsize(file),
                        "duration": duration,
                    }
                )

            # Sort by creation time, newest first
            recordings.sort(key=lambda x: x["creation_time"], reverse=True)

            return jsonify(recordings)

        @self.app.route("/api/recordings/<path:filename>/thumbnail")
        def get_recording_thumbnail(filename):
            self.logger.info(f"Getting thumbnail for recording: {filename}")
            # Use absolute path for the video file
            file_path = os.path.join(os.getcwd(), "videos", filename)
            self.logger.info(f"Path: {file_path}")
            if not os.path.exists(file_path):
                self.logger.error(f"Recording not found: {filename}")
                abort(404)

            thumbnail_dir = os.path.join(os.getcwd(), "videos", "thumbnails")
            os.makedirs(thumbnail_dir, exist_ok=True)
            thumbnail_path = os.path.join(
                thumbnail_dir, f"{os.path.splitext(filename)[0]}.jpg"
            )

            if not os.path.exists(thumbnail_path):
                try:
                    subprocess.run(
                        [
                            "ffmpeg",
                            "-y",
                            "-i",
                            file_path,
                            "-ss",
                            "00:00:01.000",
                            "-vframes",
                            "1",
                            thumbnail_path,
                        ],
                        check=True,
                    )
                except Exception as e:
                    self.logger.error(f"Error generating thumbnail: {str(e)}")
                    abort(500)

            return send_file(thumbnail_path, mimetype="image/jpeg")

        @self.app.route("/api/recordings/<path:filename>/play")
        def play_recording(filename):
            # Construct the absolute path
            filename = os.path.join(os.getcwd(), "videos", filename)

            if not os.path.exists(filename):
                self.logger.error(f"Recording not found: {filename}")
                abort(404)

            return send_file(filename, mimetype="video/mp4")

        @self.app.route("/api/recordings/<path:filename>/download")
        def download_recording(filename):
            # Construct the absolute path
            filename = os.path.join(os.getcwd(), "videos", filename)

            if not os.path.exists(filename):
                self.logger.error(f"Recording not found: {filename}")
                abort(404)

            video_path = os.path.abspath(filename)
            return send_file(video_path, mimetype="video/mp4", as_attachment=True)

        @self.app.route("/api/recordings/<path:filename>", methods=["DELETE"])
        def delete_recording(filename):
            # Construct the absolute path
            filepath = os.path.join(os.getcwd(), "videos", filename)
            if not os.path.exists(filepath):
                return jsonify({"success": False, "message": "Recording not found"})

            try:
                # Delete the recording file
                os.remove(filepath)
                self.logger.info(f"Deleted recording: {filepath}")

                # Delete the thumbnail if it exists
                name = os.path.splitext(filename)[0]
                thumbnail_filepath = os.path.join(
                    os.getcwd(), "videos", "thumbnails", f"{name}.jpg"
                )
                if os.path.exists(thumbnail_filepath):
                    os.remove(thumbnail_filepath)
                    self.logger.info(f"Deleted thumbnail: {thumbnail_filepath}")

                return jsonify({"success": True})
            except Exception as e:
                return jsonify({"success": False, "message": str(e)})
