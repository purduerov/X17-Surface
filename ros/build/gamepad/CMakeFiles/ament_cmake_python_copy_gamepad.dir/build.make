# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.27

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/benboardley/.local/lib/python3.10/site-packages/cmake/data/bin/cmake

# The command to remove a file.
RM = /home/benboardley/.local/lib/python3.10/site-packages/cmake/data/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/benboardley/src/ROV/X16-Surface/ros/gamepad

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/benboardley/src/ROV/X16-Surface/ros/build/gamepad

# Utility rule file for ament_cmake_python_copy_gamepad.

# Include any custom commands dependencies for this target.
include CMakeFiles/ament_cmake_python_copy_gamepad.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/ament_cmake_python_copy_gamepad.dir/progress.make

CMakeFiles/ament_cmake_python_copy_gamepad:
	/home/benboardley/.local/lib/python3.10/site-packages/cmake/data/bin/cmake -E copy_directory /home/benboardley/src/ROV/X16-Surface/ros/gamepad/gamepad /home/benboardley/src/ROV/X16-Surface/ros/build/gamepad/ament_cmake_python/gamepad/gamepad

ament_cmake_python_copy_gamepad: CMakeFiles/ament_cmake_python_copy_gamepad
ament_cmake_python_copy_gamepad: CMakeFiles/ament_cmake_python_copy_gamepad.dir/build.make
.PHONY : ament_cmake_python_copy_gamepad

# Rule to build all files generated by this target.
CMakeFiles/ament_cmake_python_copy_gamepad.dir/build: ament_cmake_python_copy_gamepad
.PHONY : CMakeFiles/ament_cmake_python_copy_gamepad.dir/build

CMakeFiles/ament_cmake_python_copy_gamepad.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ament_cmake_python_copy_gamepad.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ament_cmake_python_copy_gamepad.dir/clean

CMakeFiles/ament_cmake_python_copy_gamepad.dir/depend:
	cd /home/benboardley/src/ROV/X16-Surface/ros/build/gamepad && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/benboardley/src/ROV/X16-Surface/ros/gamepad /home/benboardley/src/ROV/X16-Surface/ros/gamepad /home/benboardley/src/ROV/X16-Surface/ros/build/gamepad /home/benboardley/src/ROV/X16-Surface/ros/build/gamepad /home/benboardley/src/ROV/X16-Surface/ros/build/gamepad/CMakeFiles/ament_cmake_python_copy_gamepad.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/ament_cmake_python_copy_gamepad.dir/depend

