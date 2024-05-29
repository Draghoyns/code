import nep
import time
from geometry_msgs.msg import Twist


def callback(msg):
    print("Callback get")
    print(msg)


msg_type = "dictionary"  # Message type to listen.

node = nep.node("subscriber_sample", "ROS")  # Create a new node

# Listen info inside a event loop
# sub = node.new_callback("pub_sub_test", msg_type , callback)

sub = node.new_sub("~cmd_vel", msg_type)

while True:
    is_message, msg = sub.listen()
    if is_message:

        print(msg)
    else:
        time.sleep(1)
# node.spin()
