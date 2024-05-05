#!/usr/bin/env python3

import pygame
import sys
import time

#ROS
import rclpy
from std_msgs.msg import String, Bool, Empty
from shared_msgs.msg import RovVelocityCommand, ToolsCommandMsg, ToolsMotorMsg
from geometry_msgs.msg import Twist

from config import *


tools = [0, 0, 0, 0]
motor_tools = [127,127,127,127]

SCALE_TRANSLATIONAL_X = 1.0
SCALE_TRANSLATIONAL_Y = 1.0
SCALE_TRANSLATIONAL_Z = 1.0

SCALE_ROTATIONAL_X = 1.0
SCALE_ROTATIONAL_Y = 1.0
SCALE_ROTATIONAL_Z = 1.0

TRIM_X = 0.0
TRIM_Y = 0.0
TRIM_Z = 0.0

REVERSE = 1
LOCKOUT = True
#is fine = 0 = std_mode
#is_fine = 1 = fine_mode
#is_fine = 2 = yeet mode
is_fine = 0
is_pool_centric = False
depth_lock = False
pitch_lock = False
GAMEPAD_TIMEOUT = 20 # seconds


def getMessage():
    '''Returns a RovVelocityCommand message based on the current gamepad state'''
    global gamepad_state
    global is_fine
    global is_pool_centric
    global pitch_lock
    global depth_lock

    t = Twist()

    t.linear.x = -(gamepad_state['LSY'] * SCALE_TRANSLATIONAL_X + TRIM_X) * REVERSE
    t.linear.y = -(gamepad_state['LSX'] * SCALE_TRANSLATIONAL_Y + TRIM_Y) * REVERSE
    t.linear.z = ((gamepad_state['RT'] - gamepad_state['LT']) / 2.0) * SCALE_TRANSLATIONAL_Z + TRIM_Z

    if gamepad_state['LB'] == 1:
        x = 1 * SCALE_ROTATIONAL_X
    elif gamepad_state['RB'] == 1:
        x = -1 * SCALE_ROTATIONAL_X
    else:
        x = 0.0

    t.angular.x = -x
    t.angular.y = (-gamepad_state['RSY'] * SCALE_ROTATIONAL_Y) * REVERSE
    t.angular.z = -gamepad_state['RSX'] * SCALE_ROTATIONAL_Z

    new_msg = RovVelocityCommand()
    new_msg.twist = t
    new_msg.is_fine = is_fine
    new_msg.is_pool_centric = is_pool_centric
    new_msg.depth_lock = depth_lock
    new_msg.pitch_lock = pitch_lock

    return(new_msg)


def getTools():
    '''Returns a ToolsCommandMsg message based on the current gamepad state'''
    global tools

    tm = ToolsCommandMsg()
    tm.tools = [i for i in tools]

    return tm

def getMotor():
    global motor_tools

    tmm = ToolsMotorMsg()
    tmm.tools = [i for i in motor_tools]

    return tmm


def correct_raw(raw, abbv):
    '''Corrects the raw value from the gamepad to be in the range [-1.0, 1.0]'''
    # Separate the sign from the value
    sign = (raw >= 0) * 2 - 1
    raw = abs(raw)

    # Check if the input is a trigger or a stick
    if abbv == 'LT' or abbv == 'RT':
        dead_zone = TRIGGER_DEAD_ZONE
        value_range = TRIGGER_RANGE
    else:
        dead_zone = STICK_DEAD_ZONE
        value_range = STICK_RANGE

    if raw < dead_zone:
        return 0.0

    # Remove dead zone and scale the value
    raw -= dead_zone
    raw *= value_range / (value_range - dead_zone)
    raw = 1.0 if raw > value_range else raw / value_range
    corrected = round(raw, 3)
    corrected *= sign
    return corrected


def process_event(event):
    '''Processes a pygame event'''
    global tools
    global motor_tools
    global is_fine
    global gamepad_state
    global is_pool_centric
    global depth_lock
    global pitch_lock

    # Button pressed down events
    if event.type == pygame.JOYBUTTONDOWN:
        gamepad_state[JOY_BUTTON[event.button]] = 1
        if event.button == JOY_BUTTON_KEY['A']:
            tools[0] = not tools[0]

        elif event.button == JOY_BUTTON_KEY['B']:
            tools[1] = not tools[1]

        elif event.button == JOY_BUTTON_KEY['X']:
            tools[2] = not tools[2]
        
        elif event.button == JOY_BUTTON_KEY['Y'] and LOCKOUT:
            tools[3] = not tools[3]
        
        elif event.button == JOY_BUTTON_KEY['MENU']:
            is_pool_centric = not is_pool_centric
        

    # Button released events    
    elif event.type == pygame.JOYBUTTONUP:
        gamepad_state[JOY_BUTTON[event.button]] = 0

    # DPAD buttons
    elif event.type == pygame.JOYHATMOTION:
        if event.value[1] == 1:
            if is_fine < 3:
                is_fine +=1
        elif event.value[1] == -1:
            if is_fine > 0:
                is_fine -=1
        else:
            pass
        if event.value[0] == -1:
            # add motor tool here
         #   pitch_lock = not pitch_lock
            if motor_tools[0] == 127:
                motor_tools = [180,180,180,180]
            elif motor_tools[0] == 180:
                pass
            else:
                motor_tools = [127,127,127,127]

        elif event.value[0] == 1:
            if motor_tools[0] == 127:
                motor_tools = [70,70,70,70]
            elif motor_tools[0] == 70:
                pass
            else:
                motor_tools = [127,127,127,127]
            #add motor tool here
          #  depth_lock = not depth_lock
           # is_pool_centric = True
        else:
            pass

    # Joysticks
    elif event.type == pygame.JOYAXISMOTION:
        gamepad_state[JOY_AXIS[event.axis]] = correct_raw(event.value, JOY_AXIS[event.axis])

    
    # If the gamepad is disconnected, try to reconnect it
    elif event.type == pygame.JOYDEVICEREMOVED:
        if not reconnect_gamepad():
            print("\nNo gamepad found, exiting")
            pygame.quit()
            rclpy.shutdown()
            sys.exit(0)

def pub_data():
    '''Publishes the data to the rov_velocity topic and the tools topic'''
    # Get a message to publish for the rov_velocity topic
    pub.publish(getMessage())
    # Get a message to publish for the tools topic
    pub_tools.publish(getTools())

    pub_motor_tools.publish(getMotor())

def update_gamepad():
    '''Updates the gamepad state'''
    # Get all the events from pygame and process them
    for event in pygame.event.get():
        process_event(event)


def init_pygame():
    '''Initializes pygame and the joystick'''
    global joystick
    pygame.init()
    pygame.joystick.init()
    assert pygame.joystick.get_count() == 1
    joystick = pygame.joystick.Joystick(0)


def reconnect_gamepad():
    '''Tries to reconnect the gamepad'''
    global joystick
    reconnected = False
    i = GAMEPAD_TIMEOUT
    while i >= 0 and not reconnected:
        try:
            print('Gamepad disconnected, reconnect within {:2} seconds'.format(i), end='\r')
            pygame.init()
            pygame.joystick.init()
            # make sure there is only one joystick
            if pygame.joystick.get_count() == 1:
                # get the first joystick
                joystick = pygame.joystick.Joystick(0)
                reconnected = True
            else:
                pygame.quit()
                assert False
        except:
            # wait 1 second
            pygame.time.wait(1000)
            i -= 1

    if reconnected:
        print('\nGamepad reconnected')
        joystick = pygame.joystick.Joystick(0)
        
    return reconnected


if __name__ == '__main__':
    global pub, pub_tools, data_thread, gamepad_thread

    try:
        init_pygame()
    except:
        print('No gamepad found, please connect a gamepad')
        if not reconnect_gamepad():
            print("\nNo gamepad found, exiting")
            pygame.quit()
            sys.exit(0)
    
    # Initialize the ros node
    rclpy.init()
    node = rclpy.create_node('gp_pub')

    # Create the publishers
    pub = node.create_publisher(RovVelocityCommand, 'rov_velocity', 10)
    pub_tools = node.create_publisher(ToolsCommandMsg, 'tools', 10)
    pub_motor_tools = node.create_publisher(ToolsMotorMsg, 'tools_motor', 10)

    # Create the timers
    data_thread = node.create_timer(0.1, pub_data)
    gamepad_thread = node.create_timer(0.001, update_gamepad)

    print('ready')

    rclpy.spin(node)

    data_thread.destroy()
    gamepad_thread.destroy()

    # Stop the pygame library
    pygame.quit()

    node.destroy_node()
    rclpy.shutdown()
