# Test code

#Notes:
# This will create 1 client and 1 server.
#You can create multiple clients, use timed sleeps to let messages pass back and forth and call messages on S and C to check the status of the modules.
#(you will need to handle the appropriate imports, including centrechat)

import subprocess
import CentreChat
import thread
import time

serverPort = 8046

print "======================================"
print "======================================"
print "======================================"

#For sevrer
S = CentreChat.ChatServer(serverPort) # gives this a port
thread.start_new_thread(S.Do_Loop,()) # handles mesasages

# list accumulator to store threads
ListAccum = []


#for clients
C = CentreChat.ChatClient("127.0.0.1", serverPort, "HOVERCRAFT_FULL_OF_EELS") #add Hovercraft full of eels
thread.start_new_thread(C.Do_Loop,())
ListAccum.append("HOVERCRAFT_FULL_OF_EELS")


C1 = CentreChat.ChatClient("127.0.0.1", serverPort, "GENERIC") # add Blaise
thread.start_new_thread(C1.Do_Loop,())
ListAccum.append("GENERIC")
##
C2 = CentreChat.ChatClient("127.0.0.1", serverPort, "LOOPS") # add Lupe
thread.start_new_thread(C2.Do_Loop,())
ListAccum.append("LOOPS")

time.sleep(1)

#print '______________'
C.disconnectClient()
#print '______________'


time.sleep(1)

C1.disconnectClient()
time.sleep(1)
####
C2.disconnectClient()
time.sleep(1)
##
##
print ""
print ""
print "Everyone is gone!"
