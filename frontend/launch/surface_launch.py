from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="frontend",
                executable="app.py",
                namespace="rov",
            ),
            # Node(
            #     package='controller',
            #     executable='sender.py',
            #     namespace='rov',
            # ),
            Node(
                package="mediamtx_node",
                executable="mediamtx_node.py",
                namespace="rov",
            ),
            TimerAction(
                period=5.0,  # Delay for n seconds
                actions=[
                    Node(
                        package="heartbeat_monitor",
                        executable="heartbeat_monitor.py",
                        namespace="rov",
                    ),
                    Node(
                        package='ui_subscriber',
                        executable='ui_subscriber.py',
                        namespace='rov',
                    )
                ],
            ),
        ]
    )
