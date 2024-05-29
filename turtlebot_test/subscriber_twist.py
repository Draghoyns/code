import nep
import time
from geometry_msgs.msg import Twist


def callback(msg):
    print ("Callback get")
    print (msg)

msg_type = "dictionary"           # Message type to listen.

node = nep.node("subscriber_sample", "ROS")      # Create a new node

# Listen info inside a event loop
#sub = node.new_callback("pub_sub_test", msg_type , callback)

sub = node.new_sub("~cmd_vel",msg_type)

while True :
    is_message, msg = sub.listen()
    if is_message:

        #convert dict msg : {linx, liny, linz, angx, angy, angz}
        twist = Twist()
        twist.linear.x = msg["linx"]; twist.linear.y = msg["liny"]; twist.linear.z = msg["linz"]
        twist.angular.x = msg["angx"]; twist.angular.y = msg["angy"]; twist.angular.z = msg["angz"]
        
        print(twist)
    else :
        time.sleep(1)
#node.spin()