
import pygame
import sys
import time

# ROS
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool, Empty
from shared_msgs.msg import RovVelocityCommand, ToolsCommandMsg, ToolsMotorMsg
from geometry_msgs.msg import Twist

from config import *


class GamepadNode(Node):
    def __init__(self):
        try:
            super().__init__('gp_pub')
            self.pub = self.create_publisher(
                RovVelocityCommand, 'rov_velocity', 10)
            self.pub_tools = self.create_publisher(
                ToolsCommandMsg, 'tools', 10)
            
            self.pub_motor_tools = self.create_publisher(
                ToolsMotorMsg, 'tools_motor', 10)


            self.tools = [0, 0, 0, 0]
            self.motor_tools = [127,127,127,127]

            self.SCALE_TRANSLATIONAL_X = 1.0
            self.SCALE_TRANSLATIONAL_Y = 1.0
            self.SCALE_TRANSLATIONAL_Z = 1.0

            self.SCALE_ROTATIONAL_X = 1.0
            self.SCALE_ROTATIONAL_Y = 1.0
            self.SCALE_ROTATIONAL_Z = 1.0

            self.TRIM_X = 0.0
            self.TRIM_Y = 0.0
            self.TRIM_Z = 0.0

            self.REVERSE = 1
            self.LOCKOUT = True
            self.is_fine = 0
            self.is_pool_centric = False
            self.depth_lock = False
            self.pitch_lock = False
            self.GAMEPAD_TIMEOUT = 20

            self.gamepad_state = gamepad_state

            self.init_pygame()

            self.timer_data = self.create_timer(0.1, self.pub_data)
            self.timer_gamepad = self.create_timer(0.001, self.update_gamepad)

            print('ready')

        except Exception as e:
            print(f'Error initializing gamepad: {e}')
            self.handle_gamepad_init_error()

    def handle_gamepad_init_error(self):
        print('No gamepad found, please connect a gamepad')
        if not self.reconnect_gamepad():
            print("\nNo gamepad found, exiting")
            pygame.quit()
            sys.exit(0)

    def init_pygame(self):
        pygame.init()
        pygame.joystick.init()
        assert pygame.joystick.get_count() == 1
        self.joystick = pygame.joystick.Joystick(0)

    def reconnect_gamepad(self):
        reconnected = False
        i = self.GAMEPAD_TIMEOUT
        while i >= 0 and not reconnected:
            try:
                print('Gamepad disconnected, reconnect within {:2} seconds'.format(
                    i), end='\r')
                pygame.init()
                pygame.joystick.init()
                if pygame.joystick.get_count() == 1:
                    self.joystick = pygame.joystick.Joystick(0)
                    reconnected = True
                else:
                    pygame.quit()
                    assert False
            except:
                pygame.time.wait(1000)
                i -= 1

        if reconnected:
            print('\nGamepad reconnected')
            self.joystick = pygame.joystick.Joystick(0)

        return reconnected

    def correct_raw(self, raw, abbv):
        sign = (raw >= 0) * 2 - 1
        raw = abs(raw)

        if abbv == 'LT' or abbv == 'RT':
            dead_zone = TRIGGER_DEAD_ZONE
            value_range = TRIGGER_RANGE
        else:
            dead_zone = STICK_DEAD_ZONE
            value_range = STICK_RANGE

        if raw < dead_zone:
            return 0.0

        raw -= dead_zone
        raw *= value_range / (value_range - dead_zone)
        raw = 1.0 if raw > value_range else raw / value_range
        corrected = round(raw, 3)
        corrected *= sign
        return corrected

    def process_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            self.gamepad_state[JOY_BUTTON[event.button]] = 1
            if event.button == JOY_BUTTON_KEY['A']:
                self.tools[0] = not self.tools[0]
            elif event.button == JOY_BUTTON_KEY['B']:
                self.tools[1] = not self.tools[1]
            elif event.button == JOY_BUTTON_KEY['X']:
                self.tools[2] = not self.tools[2]
            elif event.button == JOY_BUTTON_KEY['Y'] and self.LOCKOUT:
                self.tools[3] = not self.tools[3]
            elif event.button == JOY_BUTTON_KEY['START']:
                self.is_pool_centric = not self.is_pool_centric
            elif event.button == JOY_BUTTON_KEY['MENU']:
                if self.REVERSE == 1:
                    self.REVERSE = -1
                else:
                    self.REVERSE = 1

        elif event.type == pygame.JOYBUTTONUP:
            self.gamepad_state[JOY_BUTTON[event.button]] = 0

        elif event.type == pygame.JOYHATMOTION:
            if event.value[1] == 1:
                if self.is_fine < 3:
                    self.is_fine +=1
            elif event.value[1] == -1:
                if self.is_fine > 0:
                    self.is_fine -=1
            else:
                pass
            if event.value[0] == -1:
            # add motor tool here
         #   pitch_lock = not pitch_lock
                if self.motor_tools[0] == 125:
                    self.motor_tools = [250,250,250,250]
                elif self.motor_tools[0] == 180:
                    pass
                else:
                    self.motor_tools = [125,125,125,125]

            elif event.value[0] == 1:
                if self.motor_tools[0] == 125:
                    self.motor_tools = [0,0,0,0]
                elif self.motor_tools[0] == 70:
                    pass
                else:
                    self.motor_tools = [125,125,125,125]
                #add motor tool here
            else:
                pass

        elif event.type == pygame.JOYAXISMOTION:
            self.gamepad_state[JOY_AXIS[event.axis]] = self.correct_raw(
                event.value, JOY_AXIS[event.axis])

        elif event.type == pygame.JOYDEVICEREMOVED:
            if not self.reconnect_gamepad():
                print("\nNo gamepad found, exiting")
                pygame.quit()
                rclpy.shutdown()
                sys.exit(0)

    def pub_data(self):
        self.pub.publish(self.getMessage())
        self.pub_tools.publish(self.getTools())
        self.pub_motor_tools.publish(self.getMotorTools())
        

    def update_gamepad(self):
        for event in pygame.event.get():
            self.process_event(event)

    def getMessage(self):
        t = Twist()
        t.linear.x = - \
            (self.gamepad_state['LSY'] *
             self.SCALE_TRANSLATIONAL_X + self.TRIM_X) * self.REVERSE
        t.linear.y = - \
            (self.gamepad_state['LSX'] *
             self.SCALE_TRANSLATIONAL_Y + self.TRIM_Y) * self.REVERSE
        t.linear.z = ((self.gamepad_state['RT'] - self.gamepad_state['LT']
                       ) / 2.0) * self.SCALE_TRANSLATIONAL_Z + self.TRIM_Z

        if self.gamepad_state['LB'] == 1:
            x = 1 * self.SCALE_ROTATIONAL_X
        elif self.gamepad_state['RB'] == 1:
            x = -1 * self.SCALE_ROTATIONAL_X
        else:
            x = 0.0

        t.angular.x = -x
        t.angular.y = (-self.gamepad_state['RSY']
                       * self.SCALE_ROTATIONAL_Y) * self.REVERSE
        t.angular.z = -self.gamepad_state['RSX'] * self.SCALE_ROTATIONAL_Z

        new_msg = RovVelocityCommand()
        new_msg.twist = t
        new_msg.is_fine = self.is_fine
        new_msg.is_pool_centric = self.is_pool_centric
        new_msg.depth_lock = self.depth_lock
        new_msg.pitch_lock = self.pitch_lock

        return new_msg

    def getTools(self):
        tm = ToolsCommandMsg()
        tm.tools = [i for i in self.tools]
        return tm
    
    def getMotorTools(self):
        tmm = ToolsMotorMsg()
        tmm.tools = [i for i in self.motor_tools]

        return tmm
