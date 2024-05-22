# Publisher example
import nep                                # Add nep library
import time                               # Add time library
node = nep.node("sender", "ROS")                 # Define node name
conf = node.hybrid('10.105.95.233') 
pub = node.new_pub("test_topic","json", conf)   # Define topic and type of message

while True:                                 

  # Here is your code doing something ...                    
  words = ['hello','world','!', 'I', 'am', 'a', 'robot']
  msg = {}
  for i in range (len(words)):
    msg[i] = words[i]

  pub.publish(msg)		                    # Send message each second
  time.sleep(1)