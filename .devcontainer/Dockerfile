# Specify base image - ROS Jazzy is based on Ubuntu 24.04
FROM ros:jazzy
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set pip to work without virtual environment in Docker
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# CRITICAL: Install compatible setuptools for Python 3.12 and colcon-core 0.20.0
# Use setuptools 68.x-69.x range that works with both
RUN pip3 install --upgrade \
    'setuptools>=68.2.0,<70.0.0'

# Alternative: If above fails, downgrade pkg_resources separately
# RUN pip3 install --force-reinstall 'setuptools==69.5.1'

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /workspace

# Source ROS setup in bashrc
RUN echo 'source /opt/ros/jazzy/setup.bash' >> /root/.bashrc