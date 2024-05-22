# Subscriber example
import nep
import time
node = nep.node("receiver","ROS")             # Create a new nep node

def callback(msg):
    print ("Callback values")
    for key, value in msg.items():
        print (value, end=" ")
    print (msg)                         # Print new message
    # Here put your code for processing the message

sub = node.new_callback("test_topic", "json" , callback)
node.spin()