import os
import subprocess
from datetime import datetime
from flask import jsonify

class PhotoButton:
    def __init__(self, app, logger, camera_rtsp_urls):
        self.logger = logger
        self.camera_rtsp_urls = camera_rtsp_urls

        self.PHOTO_DIR = "frontend/src/frontend_utils/camera_photos"
        os.makedirs(self.PHOTO_DIR, exist_ok=True)

        @app.route("/api/photo/<camera>", methods=["POST"])
        def take_snapshot(camera):

            if camera not in self.camera_rtsp_urls:
                return jsonify({"error": "Invalid camera"}), 400

            rtsp_url = self.camera_rtsp_urls[camera]
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{self.PHOTO_DIR}/{camera}_{timestamp}.jpg"

            cmd = [
                "ffmpeg",
                "-rtsp_transport", "tcp",
                "-i", rtsp_url,

                # Give RTSP time to deliver a frame
                "-analyzeduration", "1000000",
                "-probesize", "1000000",

                "-frames:v", "1",

                "-vf",
                (
                    "drawtext="
                    "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                    f"text='{timestamp}':"
                    "x=10:y=10:"
                    "fontsize=28:"
                    "fontcolor=white:"
                    "box=1:"
                    "boxcolor=black@0.6"
                ),

                "-q:v", "2",
                filename,
                "-y"
            ]

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=8
                )

                if not os.path.exists(filename):
                    self.logger.error("FFmpeg failed")
                    self.logger.error(result.stderr)
                    return jsonify({
                        "error": "Snapshot failed",
                        "details": result.stderr
                    }), 500

                self.logger.info(f"Photo saved: {filename}")
                return jsonify({"status": "ok", "file": filename})

            except Exception as e:
                self.logger.exception("Photo capture exception")
                return jsonify({"error": str(e)}), 500