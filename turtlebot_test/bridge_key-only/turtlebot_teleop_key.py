import nep
import time
from geometry_msgs.msg import Twist
import rospy

msg_type = "string"  # Message type to listen.

node = nep.node("subscriber")  # Create a new node
sub = node.new_sub("key", msg_type)

rospy.init_node("turtlebot_teleop_bridge")
pub = rospy.Publisher("~cmd_vel", Twist, queue_size=5)

while True:
    is_message, msg = sub.listen()
    if is_message:

        # convert dict msg : {linx, liny, linz, angx, angy, angz}
        twist = Twist()
        twist.linear.x = msg["linx"]
        twist.linear.y = msg["liny"]
        twist.linear.z = msg["linz"]
        twist.angular.x = msg["angx"]
        twist.angular.y = msg["angy"]
        twist.angular.z = msg["angz"]

        print(twist)
        pub.publish(twist)
    else:
        time.sleep(1)
# node.spin()
