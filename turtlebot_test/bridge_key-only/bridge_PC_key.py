#!/usr/bin/env python

# WARNING : there will be absolutely no log associated, so you will have no idea about the speed and turn, just the input keys
# TODO : add debugging tools like display speed etc.

import nep
import time
import sys, select, termios, tty


IP = "10.105.95.233"  # IP of the remote PC
msg_type = "string"

msg = """
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
space key, k : force stop
anything else : stop smoothly
"""


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)

    else:
        key = ""

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__ == "__main__":

    settings = termios.tcgetattr(sys.stdin)

    # create the nep publisher
    node = nep.node("turtlebot_teleop")
    conf = node.hybrid(IP)
    pub = node.new_pub("key", msg_type, conf)

    print(msg)

    try:
        while 1:
            key = getKey()
            if key == "\x03":
                break
            if key != "":
                print(key)
            pub.publish(key)

    except Exception as e:
        print(e)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
