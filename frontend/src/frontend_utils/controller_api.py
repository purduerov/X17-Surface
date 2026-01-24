import os
import json
from flask import jsonify, request


class ControllerRoutes:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger
        self.config_file = os.path.join(
            os.getcwd(), "ros", "controller", "src", "mappings.json"
        )
        self.register_routes()

    def load_configs(self):
        """Load controller configurations from file"""
        try:
            # Only log at debug level for routine operations
            self.logger.debug(
                f"Loading controller configurations from {self.config_file}"
            )
            with open(self.config_file, "r") as f:
                configs = json.load(f)
                # Log config names at debug level
                config_names = list(configs.keys())
                self.logger.debug(
                    f"Loaded {len(config_names)} configurations: {config_names}"
                )
                return configs
        except FileNotFoundError:
            self.logger.warning(f"Configuration file not found: {self.config_file}")
            return {}
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in configuration file: {self.config_file}")
            return {}

    def save_config(self, mapping):
        """Save controller mapping to file"""
        pass
        self.logger.info(f"Saving configs: {mapping}")
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump(mapping, f, indent=2)

    def register_routes(self):
        """Register all controller-related routes with the Flask app"""

        @self.app.route("/api/controller/configs", methods=["GET"])
        def get_configs():
            """Get current controller button configuration"""
            configs = self.load_configs()
            # Only return a list of the keys in the mapping
            configs = list(configs.keys())
            self.logger.info(f"Current configs: {configs}")
            return jsonify(configs)

        @self.app.route("/api/controller/configs/<config_name>", methods=["GET"])
        def get_config(config_name):
            """Get a specific controller button configuration"""
            configs = self.load_configs()
            config = configs.get(config_name)
            if config:
                # self.logger.info(f"Config for {config_name}: {config}")
                return jsonify(config)
            else:
                return jsonify({"error": "Config not found"}), 404

        @self.app.route("/api/controller/configs/<config_name>", methods=["PUT"])
        def update_config(config_name):
            """Update controller button configurations"""
            configs = self.load_configs()
            new_config = request.json
            configs[config_name] = new_config
            self.save_config(configs)
            self.logger.info(f"Updated config for {config_name}: {new_config}")
            return jsonify({"message": "Config updated successfully"}), 200

        @self.app.route("/api/controller/configs/<config_name>", methods=["DELETE"])
        def delete_config(config_name):
            """Delete a specific controller button configuration"""
            configs = self.load_configs()
            if config_name in configs:
                del configs[config_name]
                self.save_config(configs)
                self.logger.info(f"Deleted config for {config_name}")
                return jsonify({"message": "Config deleted successfully"}), 200
            else:
                return jsonify({"error": "Config not found"}), 404
