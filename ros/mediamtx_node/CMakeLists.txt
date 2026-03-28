cmake_minimum_required(VERSION 3.10)
project(mediamtx_node)

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(
  PROGRAMS
    src/mediamtx_node.py
    src/mediamtx
    src/mediamtx.yml
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()