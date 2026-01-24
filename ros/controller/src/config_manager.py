#!/usr/bin/env python3

import json
import os

# import rclpy
# from rclpy.node import Node
from jsonschema import validate, ValidationError
import logging


class ConfigManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.config = None
        self.config_name = ""
        self.config_path = os.path.join(
            os.getcwd(), "ros", "controller", "src", "mappings.json"
        )
        self.schema = {
            "type": "object",
            "properties": {
                "configs": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "joystick": {
                                "type": "object",
                                "properties": {
                                    "linear": {
                                        "type": "object",
                                        "properties": {
                                            "x": {
                                                "type": "object",
                                                "properties": {
                                                    "device": {"type": "string"},
                                                    "axis": {"type": "integer"},
                                                    "scale": {"type": "number"},
                                                    "invert": {"type": "boolean"},
                                                },
                                                "required": [
                                                    "device",
                                                    "axis",
                                                    "scale",
                                                    "invert",
                                                ],
                                            },
                                            "y": {
                                                "type": "object",
                                                "properties": {
                                                    "device": {"type": "string"},
                                                    "axis": {"type": "integer"},
                                                    "scale": {"type": "number"},
                                                    "invert": {"type": "boolean"},
                                                },
                                                "required": [
                                                    "device",
                                                    "axis",
                                                    "scale",
                                                    "invert",
                                                ],
                                            },
                                            "z": {
                                                "type": "object",
                                                "properties": {
                                                    "device": {"type": "string"},
                                                    "axis": {"type": "integer"},
                                                    "scale": {"type": "number"},
                                                    "invert": {"type": "boolean"},
                                                },
                                                "required": [
                                                    "device",
                                                    "axis",
                                                    "scale",
                                                    "invert",
                                                ],
                                            },
                                        },
                                        "required": ["x", "y", "z"],
                                    },
                                    "angular": {
                                        "type": "object",
                                        "properties": {
                                            "x": {
                                                "type": "object",
                                                "properties": {
                                                    "device": {"type": "string"},
                                                    "axis": {"type": "integer"},
                                                    "scale": {"type": "number"},
                                                    "invert": {"type": "boolean"},
                                                },
                                                "required": [
                                                    "device",
                                                    "axis",
                                                    "scale",
                                                    "invert",
                                                ],
                                            },
                                            "y": {
                                                "type": "object",
                                                "properties": {
                                                    "device": {"type": "string"},
                                                    "axis": {"type": "integer"},
                                                    "scale": {"type": "number"},
                                                    "invert": {"type": "boolean"},
                                                },
                                                "required": [
                                                    "device",
                                                    "axis",
                                                    "scale",
                                                    "invert",
                                                ],
                                            },
                                            "z": {
                                                "type": "object",
                                                "properties": {
                                                    "device": {"type": "string"},
                                                    "axis": {"type": "integer"},
                                                    "scale": {"type": "number"},
                                                    "invert": {"type": "boolean"},
                                                },
                                                "required": [
                                                    "device",
                                                    "axis",
                                                    "scale",
                                                    "invert",
                                                ],
                                            },
                                        },
                                        "required": ["x", "y", "z"],
                                    },
                                },
                                "required": ["linear", "angular"],
                            },
                            "buttons": {
                                "type": "object",
                                "properties": {
                                    "tool_toggle": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "device": {"type": "string"},
                                                "button": {"type": "integer"},
                                                "action": {
                                                    "type": "string",
                                                    "enum": ["toggle", "hold"],
                                                },
                                                "tool_id": {"type": "integer"},
                                            },
                                            "required": [
                                                "device",
                                                "button",
                                                "action",
                                                "tool_id",
                                            ],
                                        },
                                    }
                                },
                                "required": ["tool_toggle"],
                            },
                            "trims": {
                                "type": "object",
                                "properties": {
                                    "x": {"type": "number"},
                                    "y": {"type": "number"},
                                    "z": {"type": "number"},
                                },
                                "required": ["x", "y", "z"],
                                "additionalProperties": False,
                            },
                            "dead_zone": {"type": "number"},
                            "scale_factors": {
                                "type": "object",
                                "properties": {
                                    "translational_x": {"type": "number"},
                                    "translational_y": {"type": "number"},
                                    "translational_z": {"type": "number"},
                                    "rotational_x": {"type": "number"},
                                    "rotational_y": {"type": "number"},
                                    "rotational_z": {"type": "number"},
                                },
                                "required": [
                                    "translational_x",
                                    "translational_y",
                                    "translational_z",
                                    "rotational_x",
                                    "rotational_y",
                                    "rotational_z",
                                ],
                                "additionalProperties": False,
                            },
                        },
                        "required": [
                            "joystick",
                            "buttons",
                            "trims",
                            "dead_zone",
                            "scale_factors",
                        ],
                    },
                }
            },
            "required": ["configs"],
        }

    def load_config(self, mapping_name="default"):
        """Load the controller mapping configuration from JSON file"""
        try:
            with open(self.config_path, "r") as f:
                configs = json.load(f)
                self.logger.info(f"Loaded configuration file: {self.config_path}")
                # Get the requested mapping from the configs collection
                if mapping_name in configs:
                    self.config = configs[mapping_name]
                    self.config_name = mapping_name
                else:
                    error_msg = (
                        f"Mapping '{mapping_name}' not found in configuration file"
                    )
                    if self.logger:
                        self.logger.error(error_msg)
                    raise ValueError(error_msg)
                if self.logger:
                    self.logger.info(f"Loaded controller configuration: {mapping_name}")
                    self.logger.info(f"{self.config}")
                return self.config

        except FileNotFoundError:
            if self.logger:
                self.logger.error(f"Configuration file not found: {self.config_path}")
            return None
        except json.JSONDecodeError:
            if self.logger:
                self.logger.error(
                    f"Invalid JSON in configuration file: {self.config_path}"
                )
            return None

    def validate_config(self):
        """Validate the loaded configuration against the schema"""
        if not self.config:
            self.load_config()

        if not self.config:
            return False

        try:
            validate(instance=self.config, schema=self.schema)
            if self.logger:
                self.logger.info("Configuration is valid.")
            return True
        except ValidationError as e:
            if self.logger:
                self.logger.error(f"Configuration validation failed: {e.message}")
            return False

    def get_axis_mapping(self, movement_type, axis):
        """Get the mapping for a specific axis"""
        if not self.config:
            self.load_config()

        if not self.config:
            return None

        # self.logger.info(f"Getting mapping for {movement_type}.{axis}")

        try:
            # mapping = self.config["joystick"][movement_type][axis]
            # self.logger.info(f"Mapping found: {mapping}")
            return self.config["joystick"][movement_type][axis]
        except KeyError:
            if self.logger:
                self.logger.error(f"No mapping found for {movement_type}.{axis}")
            return None

    def get_button_mappings(self):
        """Get all button mappings"""
        if not self.config:
            self.load_config()

        if not self.config:
            return []

        return self.config.get("buttons", {}).get("tool_toggle", [])

    def get_dead_zone(self):
        """Get the dead zone value"""
        if not self.config:
            self.load_config()

        if not self.config:
            return 0.09  # Default value

        return self.config.get("dead_zone", 0.09)

    def get_scale_factors(self):
        """Get all scale factors"""
        if not self.config:
            self.load_config()

        if not self.config:
            return {
                "translational_x": 1.0,
                "translational_y": 1.0,
                "translational_z": 1.0,
                "rotational_x": 1.0,
                "rotational_y": 1.0,
                "rotational_z": 1.0,
            }

        return self.config.get("scale_factors", {})

    def get_trims(self):
        """Get all trim values"""
        if not self.config:
            self.load_config()

        if not self.config:
            return {"x": 0.0, "y": 0.0, "z": 0.0}

        return self.config.get("trims", {})

    def get_config_name(self):
        """Get the name of the loaded configuration"""
        return self.config_name


# Main function for testing
def main():
    # Load and validate the configuration
    logger = logging.getLogger("ConfigReaderLogger")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    config_reader = ConfigManager(logger=logger)
    config_reader.load_config("default")

    # Validate the configuration
    if config_reader.validate_config():
        logger.info("Configuration is valid.")
    else:
        logger.error("Configuration is invalid.")


if __name__ == "__main__":
    main()
