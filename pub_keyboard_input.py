#!/usr/bin/env python

from __future__ import print_function

import threading

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from std_msgs.msg import String

import sys, select, termios, tty


def getKey(key_timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('pub_keyboard_input')
    publisher = rospy.Publisher('key_input', String, queue_size = 1)

    key_timeout = rospy.get_param("~key_timeout", 0.0)
    if key_timeout == 0.0:
        key_timeout = None

    pub_str = ''

    try:
        while(1):
            key = getKey(key_timeout)
            
            # Get keyboard input
            if (key == ''):
                continue
            # ^C -> quit
            elif (key == '\x03'):
                break
            # Enter input -> Publish string
            elif (key == '\r'):
                publisher.publish(pub_str)
                pub_str = ''
            else:
                pub_str += key
                print(key)

    except Exception as e:
        print(e)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
