# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_depth_comm_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED depth_comm_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(depth_comm_FOUND FALSE)
  elseif(NOT depth_comm_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(depth_comm_FOUND FALSE)
  endif()
  return()
endif()
set(_depth_comm_CONFIG_INCLUDED TRUE)

# output package information
if(NOT depth_comm_FIND_QUIETLY)
  message(STATUS "Found depth_comm: 0.0.0 (${depth_comm_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'depth_comm' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${depth_comm_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(depth_comm_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${depth_comm_DIR}/${_extra}")
endforeach()
