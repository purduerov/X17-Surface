// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from shared_msgs:msg/ImuMsg.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "shared_msgs/msg/detail/imu_msg__rosidl_typesupport_introspection_c.h"
#include "shared_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "shared_msgs/msg/detail/imu_msg__functions.h"
#include "shared_msgs/msg/detail/imu_msg__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  shared_msgs__msg__ImuMsg__init(message_memory);
}

void shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_fini_function(void * message_memory)
{
  shared_msgs__msg__ImuMsg__fini(message_memory);
}

size_t shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__size_function__ImuMsg__gyro(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_const_function__ImuMsg__gyro(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_function__ImuMsg__gyro(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__fetch_function__ImuMsg__gyro(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_const_function__ImuMsg__gyro(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__assign_function__ImuMsg__gyro(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_function__ImuMsg__gyro(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

size_t shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__size_function__ImuMsg__accel(
  const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_const_function__ImuMsg__accel(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_function__ImuMsg__accel(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__fetch_function__ImuMsg__accel(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_const_function__ImuMsg__accel(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__assign_function__ImuMsg__accel(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_function__ImuMsg__accel(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array[3] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(shared_msgs__msg__ImuMsg, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gyro",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(shared_msgs__msg__ImuMsg, gyro),  // bytes offset in struct
    NULL,  // default value
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__size_function__ImuMsg__gyro,  // size() function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_const_function__ImuMsg__gyro,  // get_const(index) function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_function__ImuMsg__gyro,  // get(index) function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__fetch_function__ImuMsg__gyro,  // fetch(index, &value) function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__assign_function__ImuMsg__gyro,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "accel",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(shared_msgs__msg__ImuMsg, accel),  // bytes offset in struct
    NULL,  // default value
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__size_function__ImuMsg__accel,  // size() function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_const_function__ImuMsg__accel,  // get_const(index) function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__get_function__ImuMsg__accel,  // get(index) function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__fetch_function__ImuMsg__accel,  // fetch(index, &value) function pointer
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__assign_function__ImuMsg__accel,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_members = {
  "shared_msgs__msg",  // message namespace
  "ImuMsg",  // message name
  3,  // number of fields
  sizeof(shared_msgs__msg__ImuMsg),
  shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array,  // message members
  shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_init_function,  // function to initialize message memory (memory has to be allocated)
  shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle = {
  0,
  &shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_shared_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, shared_msgs, msg, ImuMsg)() {
  shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle.typesupport_identifier) {
    shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &shared_msgs__msg__ImuMsg__rosidl_typesupport_introspection_c__ImuMsg_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
