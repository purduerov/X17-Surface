// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from shared_msgs:msg/RovVelocityCommand.idl
// generated code does not contain a copyright notice
#include "shared_msgs/msg/detail/rov_velocity_command__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "shared_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "shared_msgs/msg/detail/rov_velocity_command__struct.h"
#include "shared_msgs/msg/detail/rov_velocity_command__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "geometry_msgs/msg/detail/twist__functions.h"  // twist

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_shared_msgs
size_t get_serialized_size_geometry_msgs__msg__Twist(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_shared_msgs
size_t max_serialized_size_geometry_msgs__msg__Twist(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_shared_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Twist)();


using _RovVelocityCommand__ros_msg_type = shared_msgs__msg__RovVelocityCommand;

static bool _RovVelocityCommand__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _RovVelocityCommand__ros_msg_type * ros_message = static_cast<const _RovVelocityCommand__ros_msg_type *>(untyped_ros_message);
  // Field name: twist
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Twist
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->twist, cdr))
    {
      return false;
    }
  }

  // Field name: is_fine
  {
    cdr << ros_message->is_fine;
  }

  // Field name: is_pool_centric
  {
    cdr << (ros_message->is_pool_centric ? true : false);
  }

  // Field name: pitch_lock
  {
    cdr << (ros_message->pitch_lock ? true : false);
  }

  // Field name: depth_lock
  {
    cdr << (ros_message->depth_lock ? true : false);
  }

  return true;
}

static bool _RovVelocityCommand__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _RovVelocityCommand__ros_msg_type * ros_message = static_cast<_RovVelocityCommand__ros_msg_type *>(untyped_ros_message);
  // Field name: twist
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Twist
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->twist))
    {
      return false;
    }
  }

  // Field name: is_fine
  {
    cdr >> ros_message->is_fine;
  }

  // Field name: is_pool_centric
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_pool_centric = tmp ? true : false;
  }

  // Field name: pitch_lock
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->pitch_lock = tmp ? true : false;
  }

  // Field name: depth_lock
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->depth_lock = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_shared_msgs
size_t get_serialized_size_shared_msgs__msg__RovVelocityCommand(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _RovVelocityCommand__ros_msg_type * ros_message = static_cast<const _RovVelocityCommand__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name twist

  current_alignment += get_serialized_size_geometry_msgs__msg__Twist(
    &(ros_message->twist), current_alignment);
  // field.name is_fine
  {
    size_t item_size = sizeof(ros_message->is_fine);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_pool_centric
  {
    size_t item_size = sizeof(ros_message->is_pool_centric);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name pitch_lock
  {
    size_t item_size = sizeof(ros_message->pitch_lock);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name depth_lock
  {
    size_t item_size = sizeof(ros_message->depth_lock);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _RovVelocityCommand__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_shared_msgs__msg__RovVelocityCommand(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_shared_msgs
size_t max_serialized_size_shared_msgs__msg__RovVelocityCommand(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: twist
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__Twist(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: is_fine
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_pool_centric
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: pitch_lock
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: depth_lock
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = shared_msgs__msg__RovVelocityCommand;
    is_plain =
      (
      offsetof(DataType, depth_lock) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _RovVelocityCommand__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_shared_msgs__msg__RovVelocityCommand(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_RovVelocityCommand = {
  "shared_msgs::msg",
  "RovVelocityCommand",
  _RovVelocityCommand__cdr_serialize,
  _RovVelocityCommand__cdr_deserialize,
  _RovVelocityCommand__get_serialized_size,
  _RovVelocityCommand__max_serialized_size
};

static rosidl_message_type_support_t _RovVelocityCommand__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_RovVelocityCommand,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, shared_msgs, msg, RovVelocityCommand)() {
  return &_RovVelocityCommand__type_support;
}

#if defined(__cplusplus)
}
#endif
