// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from shared_msgs:msg/TempMsg.idl
// generated code does not contain a copyright notice

#ifndef SHARED_MSGS__MSG__DETAIL__TEMP_MSG__STRUCT_HPP_
#define SHARED_MSGS__MSG__DETAIL__TEMP_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__shared_msgs__msg__TempMsg __attribute__((deprecated))
#else
# define DEPRECATED__shared_msgs__msg__TempMsg __declspec(deprecated)
#endif

namespace shared_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TempMsg_
{
  using Type = TempMsg_<ContainerAllocator>;

  explicit TempMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->temperature = 0.0f;
    }
  }

  explicit TempMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->temperature = 0.0f;
    }
  }

  // field types and members
  using _temperature_type =
    float;
  _temperature_type temperature;

  // setters for named parameter idiom
  Type & set__temperature(
    const float & _arg)
  {
    this->temperature = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    shared_msgs::msg::TempMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const shared_msgs::msg::TempMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      shared_msgs::msg::TempMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      shared_msgs::msg::TempMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__shared_msgs__msg__TempMsg
    std::shared_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__shared_msgs__msg__TempMsg
    std::shared_ptr<shared_msgs::msg::TempMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TempMsg_ & other) const
  {
    if (this->temperature != other.temperature) {
      return false;
    }
    return true;
  }
  bool operator!=(const TempMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TempMsg_

// alias to use template instance with default allocator
using TempMsg =
  shared_msgs::msg::TempMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace shared_msgs

#endif  // SHARED_MSGS__MSG__DETAIL__TEMP_MSG__STRUCT_HPP_
