import subprocess

stream1_receive_cmd = "gst-launch-1.0 udpsrc port=5600 ! application/x-rtp ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false"
stream2_receive_cmd = "gst-launch-1.0 udpsrc port=5601 ! application/x-rtp ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false"
stream3_receive_cmd = "gst-launch-1.0 udpsrc port=5602 ! application/x-rtp ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false"
stream4_receive_cmd = "gst-launch-1.0 udpsrc port=5603 ! application/x-rtp ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false"


class streams:
    def __init__(self, connection):
        self.stream1_process = None
        self.stream2_process = None
        self.ssh_connection = connection

    def start(self):
        if self.ssh_connection is None:
            print("ERROR: camera streams unable to start")
            return

        print("Receiving camera stream 1...")
        self.stream1_process = subprocess.Popen(
            stream1_receive_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.stream1_process is not None:
            print(f"Process {self.stream1_process.pid} started")
        else:
            print("Failed to receive camera stream 1")

        print("Receiving camera stream 2...")
        self.stream2_process = subprocess.Popen(
            stream2_receive_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.stream2_process is not None:
            print(f"Process {self.stream2_process.pid} started")
        else:
            print("Failed to receive camera stream 2")
            
        print("Receiving camera stream 3...")
        self.stream3_process = subprocess.Popen(
            stream3_receive_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.stream3_process is not None:
            print(f"Process {self.stream3_process.pid} started")
        else:
            print("Failed to receive camera stream 3")

        print("Receiving camera stream 4...")
        self.stream4_process = subprocess.Popen(
            stream4_receive_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.stream4_process is not None:
            print(f"Process {self.stream4_process.pid} started")
        else:
            print("Failed to receive camera stream 2")

    def stop(self):
        if self.stream1_process is not None:
            self.stream1_process.kill()
            print(f"Process {self.stream1_process.pid} killed")
        if self.stream2_process is not None:
            self.stream2_process.kill()
            print(f"Process {self.stream2_process.pid} killed")
        if self.stream3_process is not None:
            self.stream3_process.kill()
            print(f"Process {self.stream3_process.pid} killed")
        if self.stream4_process is not None:
            self.stream4_process.kill()
            print(f"Process {self.stream4_process.pid} killed")
