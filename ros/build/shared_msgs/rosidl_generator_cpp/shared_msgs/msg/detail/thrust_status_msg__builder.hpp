// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from shared_msgs:msg/ThrustStatusMsg.idl
// generated code does not contain a copyright notice

#ifndef SHARED_MSGS__MSG__DETAIL__THRUST_STATUS_MSG__BUILDER_HPP_
#define SHARED_MSGS__MSG__DETAIL__THRUST_STATUS_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "shared_msgs/msg/detail/thrust_status_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace shared_msgs
{

namespace msg
{

namespace builder
{

class Init_ThrustStatusMsg_status
{
public:
  Init_ThrustStatusMsg_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::shared_msgs::msg::ThrustStatusMsg status(::shared_msgs::msg::ThrustStatusMsg::_status_type arg)
  {
    msg_.status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::shared_msgs::msg::ThrustStatusMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::shared_msgs::msg::ThrustStatusMsg>()
{
  return shared_msgs::msg::builder::Init_ThrustStatusMsg_status();
}

}  // namespace shared_msgs

#endif  // SHARED_MSGS__MSG__DETAIL__THRUST_STATUS_MSG__BUILDER_HPP_
