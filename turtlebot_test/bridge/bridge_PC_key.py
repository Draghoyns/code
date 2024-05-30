#!/usr/bin/env python

from geometry_msgs.msg import Twist
import nep
import time
import sys, select, termios, tty


IP = "10.105.95.233"  # IP of the remote PC
msg_type = "dictionary"

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

moveBindings = {
    "i": (1, 0),
    "o": (1, -1),
    "j": (0, 1),
    "l": (0, -1),
    "u": (1, 1),
    ",": (-1, 0),
    ".": (-1, 1),
    "m": (-1, -1),
}

speedBindings = {
    "q": (1.1, 1.1),
    "z": (0.9, 0.9),
    "w": (1.1, 1),
    "x": (0.9, 1),
    "e": (1, 1.1),
    "c": (1, 0.9),
}


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ""

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    print(key)
    return key


speed = 0.2
turn = 1


def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)


if __name__ == "__main__":

    settings = termios.tcgetattr(sys.stdin)

    # create the nep publisher
    node = nep.node("turtlebot_teleop")
    conf = node.hybrid(IP)
    pub = node.new_pub("velo", msg_type, conf)

    message = {}

    x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    try:
        print(msg)
        print(vels(speed, turn))
        while 1:
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0

                print(vels(speed, turn))
                if status == 14:
                    print(msg)
                status = (status + 1) % 15
            elif key == " " or key == "k":
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if key == "\x03":
                    break

            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min(target_speed, control_speed + 0.02)
            elif target_speed < control_speed:
                control_speed = max(target_speed, control_speed - 0.02)
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min(target_turn, control_turn + 0.1)
            elif target_turn < control_turn:
                control_turn = max(target_turn, control_turn - 0.1)
            else:
                control_turn = target_turn

            message["linx"] = control_speed
            message["liny"] = 0
            message["linz"] = 0
            message["angx"] = 0
            message["angy"] = 0
            message["angz"] = control_turn
            pub.publish(message)

    except Exception as e:
        print(e)

    finally:

        message["linx"] = 0
        message["liny"] = 0
        message["linz"] = 0
        message["angx"] = 0
        message["angy"] = 0
        message["angz"] = 0

        print(message)
        pub.publish(message)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
