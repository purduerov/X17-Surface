from std_msgs.msg import String, Bool
from shared_msgs.msg import FinalThrustMsg
import json


def handle_frontend_event(node, event, data):
    """
    Handle frontend events sent via Socket.IO and publish to appropriate ROS topics.

    Args:
        node: The ROS node instance
        event: The event name (string)
        data: The event data (dict or string)
    """
    # Handle thruster control events
    if event == "frontend-sendThrusterValues":
        # Lazy initialization of publisher
        if not hasattr(node, "final_thrust_pub") or node.final_thrust_pub is None:
            node.final_thrust_pub = node.create_publisher(
                FinalThrustMsg, "final_thrust", 10
            )
            node.get_logger().debug("Created final_thrust publisher")

        # Create and publish thrust message
        thrust_msg = FinalThrustMsg()
        thrust_msg.thrusters = list(data.values())
        node.final_thrust_pub.publish(thrust_msg)
        # Don't log every thrust command as they're too frequent

    # Handle controller mapping updates
    elif event == "frontend-updateControllerMapping":
        # Parse data if needed
        if isinstance(data, str):
            data = json.loads(data)

        mapping_name = data.get("name")
        if not mapping_name:
            node.get_logger().warning(
                f"Invalid controller mapping data received: {data}"
            )
            return

        # Log only mapping changes, not every mapping message
        node.get_logger().info(f"Updating controller mapping to: {mapping_name}")

        # Lazy initialization of publisher
        if (
            not hasattr(node, "controller_mapping_pub")
            or node.controller_mapping_pub is None
        ):
            node.controller_mapping_pub = node.create_publisher(
                String, "controller_mapping", 10
            )
            node.get_logger().debug("Created controller_mapping publisher")

        # Create and publish mapping message
        controller_mapping = String()
        controller_mapping.data = mapping_name
        node.controller_mapping_pub.publish(controller_mapping)

    elif event == "frontend-resetThrusters":
        if not hasattr(node, "reset_thrust_pub") or node.reset_thrust_pub is None:
            node.reset_thrust_pub = node.create_publisher(Bool, "reset_thrusters", 10)
            node.get_logger().debug("Created reset_thrusters publisher")

        reset_msg = Bool()
        reset_msg.data = True
        node.reset_thrust_pub.publish(reset_msg)
        # Log reset event at debug level
        node.get_logger().debug("Reset thrusters command sent")

    # Add a generic handler for other events
    else:
        # Only log unhandled events at debug level
        node.get_logger().debug(f"Unhandled frontend event: {event}")
