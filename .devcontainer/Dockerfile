# Specify base image - ROS Jazzy is based on Ubuntu 24.04
FROM ros:jazzy
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10-pip \
    python3.10-venv \
    python3.10-dev \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set pip to work without virtual environment in Docker
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Set working directory
WORKDIR /workspace

# Source ROS setup in bashrc
RUN echo 'source /opt/ros/jazzy/setup.bash' >> /root/.bashrc