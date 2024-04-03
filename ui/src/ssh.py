import paramiko
import netifaces
import time
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=f"{os.getcwd()}/src/X16-Surface/.env")


class ssh:
    def __init__(self):
        self.ssh_host = os.getenv("HOST_IP")
        self.ssh_username = os.getenv("HOST_USERNAME")
        self.ssh_password = os.getenv("HOST_PASSWORD")
        self.device_name1 = os.getenv("DEVICE_NAME1")
        self.device_name2 = os.getenv("DEVICE_NAME2")
        self.device_name3 = os.getenv("DEVICE_NAME3")
        self.device_name4 = os.getenv("DEVICE_NAME4")
        self.ssh_client = None
        self.pid_list = list()
        self.connection = None

    def connect(self):
        try:
            # getting the local ip address
            ip = self.get_ip()
            print(f"Local IP address: {ip}")
            #ros_id = 69
            # commands to launch on the pi
            ros2_source_cmd ="source ~/.bashrc >> ~/ros2_ws/startup_logs/sourcebash.txt && export ROS_DOMAIN_ID=69 && source ros2_ws/install/setup.bash >> ~/ros2_ws/startup_logs/source.txt && echo $ROS_DOMAIN_ID >> ~/ros2_ws/startup_logs/domain_id_tmux"
            ros2_launch_cmd = "ros2 launch rov_launch run_rov_launch.xml >> ~/ros2_ws/startup_logs/launch.txt"
            stream1_launch_cmd = f"gst-launch-1.0 -v v4l2src device={self.device_name1} ! video/x-h264, width=1920,height=1080! h264parse ! queue ! rtph264pay config-interval=10 pt=96 ! udpsink host={ip} port=5600 sync=false buffer-size=1048576 & echo $! > pid.txt"
            stream2_launch_cmd = f"gst-launch-1.0 -v v4l2src device={self.device_name2} ! video/x-h264, width=1920,height=1080! h264parse ! queue ! rtph264pay config-interval=10 pt=96 ! udpsink host={ip} port=5601 sync=false buffer-size=1048576 & echo $! > pid.txt"
            stream3_launch_cmd = f"gst-launch-1.0 -v v4l2src device={self.device_name3} ! video/x-h264, width=1920,height=1080! h264parse ! queue ! rtph264pay config-interval=10 pt=96 ! udpsink host={ip} port=5602 sync=false buffer-size=1048576 & echo $! > pid.txt"
            stream4_launch_cmd = f"gst-launch-1.0 -v v4l2src device={self.device_name4} ! video/x-h264, width=1920,height=1080! h264parse ! queue ! rtph264pay config-interval=10 pt=96 ! udpsink host={ip} port=5603 sync=false buffer-size=1048576 & echo $! > pid.txt"
          #  print(stream1_launch_cmd)
          #  print(stream1_launch_cmd)

            # establishing the ssh connection
            print("Establishing SSH connection...")
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.ssh_client.connect(
                self.ssh_host,
                username=self.ssh_username,
                password=self.ssh_password,
                timeout=5,
            )
            if self.ssh_client is not None:
                print("SSH connection established")
                self.connection = True
            else:
                print("ERROR: SSH connection failed")
                return

            # launching the ros2 nodes on the pi
            self.launch_ros2_nodes(ros2_source_cmd, ros2_launch_cmd)

            # launching the camera streams on the pi
            self.launch_stream(1, stream1_launch_cmd)
            self.launch_stream(2, stream2_launch_cmd)
            self.launch_stream(3, stream3_launch_cmd)
            self.launch_stream(4, stream4_launch_cmd)

            return self.connection

        except Exception as e:
            print(f"ERROR: {e}")
            return

    def close(self):
        # killing each process
        # if self.pid_list is not None:
        #     for pid in self.pid_list:
        #         self.ssh_client.exec_command("kill " + pid)
        if self.ssh_client is not None:
            self.ssh_client.exec_command(
                "ps aux | grep ros2 | awk '{print $2}' | xargs kill -9 && tmux kill-session -t ros2_session")

        # closing the ssh connection
        if self.ssh_client is not None:
            self.ssh_client.close()
            print("SSH connection closed")

    def get_ip(self):
        try:
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip_address = addr_info["addr"]
                        if ip_address.startswith("192.168.1."):
                            return ip_address
        except Exception as e:
            print(f"ERROR: {e}")

    def launch_ros2_nodes(self, ros2_source_cmd, ros2_launch_cmd):
        try:
            print("Launching ROS2 nodes...")

            # Concatenate the commands and run them in a single exec_command call
            full_command = f"tmux new-session -d -s ros2_session 'bash -c \"{ros2_source_cmd} && {ros2_launch_cmd}\"'"
            self.ssh_client.exec_command(full_command)

            time.sleep(1)
            print("ROS2 nodes launched")
        except Exception as e:
            print(f"ERROR: {e}")

    def launch_stream(self, num, cmd):
        try:
            print(f"Launching camera stream {num}...")
            self.ssh_client.exec_command(cmd)
            time.sleep(1)
            __, stdout, __ = self.ssh_client.exec_command("cat pid.txt")
            self.pid = stdout.read().decode("utf-8").strip()
            self.pid_list.append(self.pid)
            print(f"Process {self.pid} started")
        except Exception as e:
            print(f"ERROR: {e}")


# launch command for camera stream 1
# gst-launch-1.0 -v v4l2src device=/dev/video0 ! image/jpeg, width=1920, height=1080, framerate=30/1 ! jpegparse ! rtpjpegpay ! udpsink host=10.0.0.103 port=5600 sync=false buffer-size=1048576
# gst-launch-1.0 -v udpsrc port=5600 ! application/x-rtp, payload=26 ! rtpjpegdepay ! jpegdec ! autovideosink

# launch command for camera stream 2
