#!/bin/bash

# Define directories to be removed
normal_directories=("log" "build")
purge_directories=("install" "logs")
executable="ros/mediamtx_node/src/mediamtx"

# Function to display help message
show_help() {
    echo "Usage: $0 [OPTION]"
    echo "Clean up directories and files."
    echo
    echo "Options:"
    echo "  -h, --help    Show this help message and exit"
    echo "  -p, --purge   Purge additional directories and files"
    echo
    echo "By default, this script removes:"
    echo "  - log"
    echo "  - build"
    echo
    echo "When run with --purge, it additionally removes:"
    echo "  - install"
    echo "  - logs"
    echo "  - $executable"
}

# Check for the help argument
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Check for the purge argument
purge=false
if [[ "$1" == "--purge" || "$1" == "-p" ]]; then
    purge=true
fi

# Function to remove directories
remove_directories() {
    local dirs=("$@")
    for dir in "${dirs[@]}"; do
        if [ -d "$dir" ]; then
            echo "Removing directory: $dir"
            rm -rf "$dir"
        else
            echo "Directory $dir does not exist."
        fi
    done
}

# Remove normal directories
remove_directories "${normal_directories[@]}"

# If purge is true, remove additional directories and executable
if [ "$purge" = true ]; then
    remove_directories "${purge_directories[@]}"
    if [ -f "$executable" ]; then
        echo "Removing executable: $executable"
        rm -f "$executable"
    else
        echo "Executable $executable does not exist."
    fi
fi

source /opt/ros/jazzy/setup.bash

echo "Cleanup complete."