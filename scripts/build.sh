#!/bin/bash

# Check if mediamtx executable exists in /ros/mediamtx
if [ ! -f ./ros/mediamtx_node/src/mediamtx ]; then
    echo "mediamtx executable not found in ./ros/mediamtx_node/src"
    # Ask the user if they would like to run the install_mediamtx.sh script
    read -p "Would you like to run the install_mediamtx.sh script? (y/n): " run_install_mediamtx
    if [ "$run_install_mediamtx" == "y" ]; then
        ./scripts/install_mediamtx.sh
    else
        echo "Please run scripts/install_mediamtx.sh first"
        exit 1
    fi
fi


# Create .env file if it does not exist
if [ ! -f .env ]; then
    echo "The .env file does not exist. Creating a new .env file."
    touch .env
else
    # Source the .env file if it exists
    source .env
fi


# Check if the environment variables from a list exist (lists do not have commas in bash ex: env_vars=("VAR1" "VAR2"))
### --------------------------- ###
# ADD ENVIRONMENT VARIABLES HERE  #
### --------------------------- ###
env_vars=("FLASK_PORT")
env_vars_default=("5013")

for i in "${!env_vars[@]}"; do
    var="${env_vars[$i]}"
    default="${env_vars_default[$i]}"
    if [ -z "${!var}" ]; then
        echo "Environment variable $var is not set. Using the default value: $default"
        echo "$var=$default" >> .env
    fi
done

# Build the ROS 2 workspace
source /opt/ros/humble/setup.bash
colcon build
. install/setup.bash
export ROS_DOMAIN_ID=69