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
CMAKE_SOURCE_DIR = /home/benboardley/src/ROV/X16-Surface/ros/thrusters

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/benboardley/src/ROV/X16-Surface/ros/build/thrusters

# Utility rule file for ament_cmake_python_copy_thrusters.

# Include any custom commands dependencies for this target.
include CMakeFiles/ament_cmake_python_copy_thrusters.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/ament_cmake_python_copy_thrusters.dir/progress.make

CMakeFiles/ament_cmake_python_copy_thrusters:
	/home/benboardley/.local/lib/python3.10/site-packages/cmake/data/bin/cmake -E copy_directory /home/benboardley/src/ROV/X16-Surface/ros/thrusters/thrusters /home/benboardley/src/ROV/X16-Surface/ros/build/thrusters/ament_cmake_python/thrusters/thrusters

ament_cmake_python_copy_thrusters: CMakeFiles/ament_cmake_python_copy_thrusters
ament_cmake_python_copy_thrusters: CMakeFiles/ament_cmake_python_copy_thrusters.dir/build.make
.PHONY : ament_cmake_python_copy_thrusters

# Rule to build all files generated by this target.
CMakeFiles/ament_cmake_python_copy_thrusters.dir/build: ament_cmake_python_copy_thrusters
.PHONY : CMakeFiles/ament_cmake_python_copy_thrusters.dir/build

CMakeFiles/ament_cmake_python_copy_thrusters.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/ament_cmake_python_copy_thrusters.dir/cmake_clean.cmake
.PHONY : CMakeFiles/ament_cmake_python_copy_thrusters.dir/clean

CMakeFiles/ament_cmake_python_copy_thrusters.dir/depend:
	cd /home/benboardley/src/ROV/X16-Surface/ros/build/thrusters && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/benboardley/src/ROV/X16-Surface/ros/thrusters /home/benboardley/src/ROV/X16-Surface/ros/thrusters /home/benboardley/src/ROV/X16-Surface/ros/build/thrusters /home/benboardley/src/ROV/X16-Surface/ros/build/thrusters /home/benboardley/src/ROV/X16-Surface/ros/build/thrusters/CMakeFiles/ament_cmake_python_copy_thrusters.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/ament_cmake_python_copy_thrusters.dir/depend

