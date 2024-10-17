#!/usr/bin/env python3

import pygame
import sys
import time

#ROS
import rclpy
from std_msgs.msg import String, Bool, Empty
from shared_msgs.msg import RovVelocityCommand, ToolsCommandMsg
from geometry_msgs.msg import Twist

from config import *


tools = [0, 0, 0, 0, 0]

SCALE_TRANSLATIONAL_X = 1.0
SCALE_TRANSLATIONAL_Y = 1.0
SCALE_TRANSLATIONAL_Z = 1.0

SCALE_ROTATIONAL_X = 1.0
SCALE_ROTATIONAL_Y = 1.0
SCALE_ROTATIONAL_Z = 1.0

REVERSE = 1

TRIM_X = 0.0
TRIM_Y = 0.0
TRIM_Z = 0.0

GAMEPAD_TIMEOUT = 20 # seconds

JOYSTICK_NAME = "Thrustmaster T.16000M"
THROTTLE_NAME = "Thrustmaster TWCS Throttle"


class Contoller:
    def __init__(self):

        self.joystick = None
        self.throttle = None
        self.joystick_id = 0
        self.throttle_id = 0

        self.reverse = 1
        self.lockout = True
        self.is_fine = 0
        self.is_pool_centric = False
        self.depth_lock = False
        self.pitch_lock = False
        self.joystick_axis_state = joystick_axis_state
        self.joystick_button_state = joystick_button_state
        self.throttle_axis_state = throttle_axis_state
        self.throttle_button_state = throttle_button_state
        self.mapping = 0 # 0, 1, 2, 3

        # Initialize the ros node
        rclpy.init()
        self.node = rclpy.create_node('gp_pub')
        
        try:
            self.init_pygame()
        except:
            node.get_logger().info('Controllers not found. Please make sure both the joystick and throttle are connected')
            if not reconnect_gamepad():
                node.get_logger().info("\nNo gamepad found, exiting")
                pygame.quit()
                sys.exit(0)
        
        # Create the publishers
        self.pub = self.node.create_publisher(RovVelocityCommand, '/rov_velocity', 10)
        self.pub_tools = self.node.create_publisher(ToolsCommandMsg, 'tools', 10)

        # Create the timers
        self.data_thread = self.node.create_timer(0.1, self.pub_data)
        self.gamepad_thread = self.node.create_timer(0.001, self.update_gamepad)

        self.node.get_logger().info('Controllers initialized')

        rclpy.spin(self.node)

        self.data_thread.destroy()
        self.gamepad_thread.destroy()

        # Stop the pygame library
        pygame.quit()

        self.node.destroy_node()
        rclpy.shutdown()


    def init_pygame(self):
        '''Initializes pygame and the joystick'''
        pygame.init()
        pygame.joystick.init()
        # Should be two joysticks
        assert pygame.joystick.get_count() == 2

        # Determine which joystick is the joystick and which is the throttle
        for i in range(pygame.joystick.get_count()):
            if pygame.joystick.Joystick(i).get_name() == JOYSTICK_NAME:
                self.joystick = pygame.joystick.Joystick(i)
                self.joystick_id = i
            if pygame.joystick.Joystick(i).get_name() == THROTTLE_NAME:
                self.throttle = pygame.joystick.Joystick(i)
                self.throttle_id = i


    def update_gamepad(self):
        '''Updates the gamepad state'''
        # Get all the events from pygame and process them
        for event in pygame.event.get():
            self.process_event(event)



    def reconnect_gamepad(self):
        exit(0)


    def correct_raw(self, raw):
        '''Corrects the raw value from the gamepad to be in the range [-1.0, 1.0]'''
        if raw > 0:
            if raw >= STICK_DEAD_ZONE:
                return -raw
            elif raw > 1:
                return -1
            else:
                return 0
        
        if raw < 0:
            if raw <= -STICK_DEAD_ZONE:
                return -raw
            elif raw < -1:
                return 1
            else:
                return 0


    def process_event(self, event):
        '''Processes a pygame event'''
        # Check if the event is a joyaxismotion event
        if event.type == pygame.JOYAXISMOTION:
            # Check if the event is from the joystick or the throttle
            if event.joy == self.joystick_id:
                self.joystick_axis_state[event.axis] = self.correct_raw(event.value)
            elif event.joy == self.throttle_id:
                self.throttle_axis_state[event.axis] = self.correct_raw(event.value)

        # Check if the event is a joybuttondown event
        elif event.type == pygame.JOYBUTTONDOWN:
            # Check if the event is from the joystick or the throttle
            if event.joy == self.joystick_id:
                self.joystick_button_state[event.button] = 1
            elif event.joy == self.throttle_id:
                self.throttle_button_state[event.button] = 1

        # Check if the event is a joybuttonup event
        elif event.type == pygame.JOYBUTTONUP:
            # Check if the event is from the joystick or the throttle
            if event.joy == self.joystick_id:
                self.joystick_button_state[event.button] = 0
            elif event.joy == self.throttle_id:
                self.throttle_button_state[event.button] = 0

        # Check if the event is a joydeviceremoved event
        elif event.type == pygame.JOYDEVICEREMOVED:
            # Try to reconnect the gamepad
            if not self.reconnect_gamepad():
                self.node.get_logger().info("\nNo gamepad found, exiting")
                pygame.quit()
                sys.exit(0)

    def pub_data(self):
        '''Publishes the data to the rov_velocity topic and the tools topic'''
        # Get a message to publish for the rov_velocity topic
        self.pub.publish(self.getMessage())
        # Get a message to publish for the tools topic
        # pub_tools.publish(self.getTools())



        

    def getMessage(self):
        '''Returns a RovVelocityCommand message based on the current gamepad state'''
        global button_state
        global axis_state
        global hat_state
        global is_fine
        global is_pool_centric
        global pitch_lock
        global depth_lock

        t = Twist()

        t.linear.x = -(self.throttle_axis_state[2] * SCALE_TRANSLATIONAL_X + TRIM_X) * REVERSE
        t.linear.y = -(self.throttle_axis_state[5] * SCALE_TRANSLATIONAL_Y + TRIM_Y) * REVERSE
        t.linear.z = -(self.throttle_axis_state[1] * SCALE_TRANSLATIONAL_Y + TRIM_Y) * REVERSE
        
        t.angular.x = -(self.joystick_axis_state[1] * SCALE_ROTATIONAL_X) * REVERSE
        t.angular.y = -(self.joystick_axis_state[0] * SCALE_ROTATIONAL_Y) * REVERSE
        t.angular.z = -(self.joystick_axis_state[2] * SCALE_ROTATIONAL_Z) * REVERSE

        new_msg = RovVelocityCommand()
        new_msg.twist = t
        new_msg.is_fine = self.is_fine
        new_msg.is_pool_centric = self.is_pool_centric
        new_msg.depth_lock = self.depth_lock
        new_msg.pitch_lock = self.pitch_lock

        return(new_msg)


def getTools():
    '''Returns a ToolsCommandMsg message based on the current gamepad state'''
    global tools

    tm = ToolsCommandMsg()
    tm.tools = [i for i in tools]

    return tm




def reconnect_gamepad():
    '''Tries to reconnect the gamepad'''
    global joystick, throttle
    reconnected = False
    i = GAMEPAD_TIMEOUT
    while i >= 0 and not reconnected:
        try:
            node.get_logger().info('Gamepad disconnected, reconnect within {:2} seconds'.format(i))
            pygame.init()
            pygame.joystick.init()
            # make sure there are two joysticks
            if pygame.joystick.get_count() == 2:
                # get the first joystick
                joystick = pygame.joystick.Joystick(0)
                throttle = pygame.joystick.Joystick(1)
                reconnected = True
            else:
                pygame.quit()
                assert False
        except:
            # wait 1 second
            pygame.time.wait(1000)
            i -= 1

    if reconnected:
        node.get_logger().info('\nGamepad reconnected')
        joystick = pygame.joystick.Joystick(0)
        throttle = pygame.joystick.Joystick(1)
        
    return reconnected


if __name__ == '__main__':
    controller = Contoller()
