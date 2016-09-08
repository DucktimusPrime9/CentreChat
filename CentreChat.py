#########################################
#                                       #
#           Lab 5 Chat Client           #
#                                       #
#########################################
#                                       #
#              Centre Chat              #
#                                       #
#########################################
#                                       #
#           Guadalupe Delgado           #
#                                       #
#########################################

#!/usr/bin/python

import socket
import random
import time
import select
import sys
import traceback

#Client Class

class ChatClient:

        def __init__(self, serverName, serverPort, HandleName):
                self.serverName = serverName
                self.serverPort = serverPort
                self.HandleName = HandleName
                self.serverAddress = (self.serverName, self.serverPort)
                self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.clientSocket.bind(("",0))
                self.MyAddress = ("127.0.0.1",self.clientSocket.getsockname()[1])
                self.SequenceNumber = 0
                self.ClientReqMessage = "CONNECT\n%s\n%d\n\n"%(self.HandleName, self.SequenceNumber)
                self.clientSocket.sendto(self.ClientReqMessage, self.serverAddress)

         # Waits for an ACK
        def WaitACK(self): # this state 0
                ReadReady, OutReady, ExceptReady = select.select([self.clientSocket], [], [], 1)
                if ReadReady == []:
                        self.clientSocket.sendto(self.ClientReqMessage, self.serverAddress)
                        print "time out"
                        return 0
                else:
                        RequestMessage, serverAddress = self.clientSocket.recvfrom(1500)
                        if(serverAddress == self.serverAddress):
                                if(self.KeyWord(RequestMessage) == "ACK"):
                                        self.SequenceNumber = (self.SequenceNumber + 1)%1024
                                        return 1

                        return 0

        def ChatState(self): #state 1
                ReadReady, OutReady, ExceptReady = select.select([self.clientSocket], [], [], 1)
                if ReadReady != []:
                        RequestMessage, serverAddress = self.clientSocket.recvfrom(1500)
                        if(serverAddress == self.MyAddress):
                                if(self.KeyWord(RequestMessage) == "DISCONNECT"):
                                        self.ClientReqMessage = "DISCONNECT\n%s\n%d\n\n"%(self.HandleName, self.SequenceNumber)
                                        self.clientSocket.sendto(self.ClientReqMessage, self.serverAddress)
                                        #print "  chat state: disconnect (ok)" + "\n"
                                        return 3
                        return 0

                else:
                        return 1


         # The Client waits for an ACK to disconnect
        def WaitDisconnectACK(self): #state 2
                ReadReady, OutReady, ExceptReady = select.select([self.clientSocket], [], [], 1)
                if ReadReady == []:
                        self.clientSocket.sendto(self.ClientReqMessage, self.serverAddress)
                        return 2
                else:
                        RequestMessage, serverAddress = self.clientSocket.recvfrom(1500)
                        print RequestMessage
                        if(serverAddress == self.serverAddress):
                                if(self.KeyWord(RequestMessage) == "ACK"):
                                        if(self.SequenceNumber == self.GetSequenceNum(RequestMessage)):
                                                #print "oooooooooooooooooooo"
                                                return 3
                                return 2
                        else:
                                return 2

        #get the sequence number
        def GetSequenceNum(self, Message):
                 if(self.KeyWord(Message) == "ACK"):
                        Sequence =Message[Message.find("\n") + 1:Message.find("\n\n")]
                        return Sequence

         #gets Keyword of the header
        def KeyWord(self, Message):
                HeaderKeyWord = Message[:Message.find("\n")]
                return HeaderKeyWord

        #The client can change between 4 states
        def Do_Loop(self):
                try:
                        Open = True
                        SwitchState = 0
                        while Open:
                                if(SwitchState == 0):
                                        SwitchState = self.WaitACK()
                                        #print "  WaitACK works"
                                elif(SwitchState == 1):
                                        SwitchState = self.ChatState()


                                        #print "Chatstate works"
##                                elif(SwitchState == 4):
##                                        SwitchState = self.ClientMessages()
##                                        #print "Client Messages works"
                                elif(SwitchState == 2):
                                        SwitchState = self.WaitDisconnectACK()
                                        #print "WaitDisconnectAck works"
                                elif(SwitchState == 3):
                                        Open = False
                                        #self.clientSocket.Close()
                                else:

                                        print "something went wrong in do_loop Client"
                                        break
                except Exception, e:
                        print traceback.format_exc()

                        self.clientSocket.Close()




        #Disconnect from server
        def disconnectClient(self):
                self.ClientReqMessage = "DISCONNECT\n%s\n%d\n\n"%(self.HandleName, self.SequenceNumber)
                self.clientSocket.sendto(self.ClientReqMessage, self.MyAddress)
                #print "disconnect from server(ok) \n "



################################################################################################################################

#Server class

class ChatServer:

        def __init__(self, serverPort):
                self.clients = [] # address, handle, server seq, exp seq number
                self.Message = []
                self.serverPort = serverPort
                self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.serverSocket.bind(('', serverPort))

        # get clients...find handleName
        def getClients(self):
                Init_List = []
                for client in self.clients:
                        #get the handle of the clients
                        Init_list.append(client[1])
                Init_List.sort()
                return Init_List

        # To get the handle from the message which is the second index in the message
        def getHandle(self, Message):
               FirstIndex = Message.find("\n") # finds the first index (ClientAddress)
               Handle = Message[FirstIndex + 1:Message.find("\n",FirstIndex + 1)] #finds the 2nd index (handle)
               return Handle # returns handle

        def KeyWordGiven(self, Message):
               KeyGiven = Message[:Message.find("\n")]
               return KeyGiven
  #################################################################################################################################################################
        def SendACK(self):
                # select... timeout for server
                ReadReady, OutReady, ExceptReady = select.select([self.serverSocket], [], [], 1) # actual protocol asks for 20 seconds here
                if ReadReady != []:
                        Message, ClientAddress = self.serverSocket.recvfrom(1500)


                                #if the message keyword is CONNECT...this is to add client
                        if(self.KeyWordGiven(Message) == "CONNECT"):
                                        print "\n Client wants to connect"
                                        ServerMessage = "ACK\n%d\n\n"%(0)


                                        self.serverSocket.sendto(ServerMessage, ClientAddress)
                                        self.clients.append((ClientAddress, self.getHandle(Message), 0, 1))
                                        print self.getHandle(Message), "\n was successfully added!!" #, self.clients

                                        print "\n Welcome!!"
                                        return 0


                                # if the message keyword is DISCONNECT...this is to remove client
                        elif (self.KeyWordGiven(Message) == "DISCONNECT"):
                                        print "\n Client wants to disconnect"

                                        ServerMessage = "ACK\n%d\n\n"%(1)

                                        self.serverSocket.sendto(ServerMessage, ClientAddress)
                                        self.removeClients(ClientAddress)
                                        print self.getHandle(Message), "Client was Successfully removed"
                                        print " Have a great day!!"
                                        return 0
                        else:
                                return 0

                else:
                        return 0

         # Method to remove clients based on address
        def removeClients(self, ClientAddress):
                index = 0
                #print type(self.clients)
                #time.sleep(3)
                for client in self.clients:
                        FirstAddress = client[0]
                        #print FirstAddress
                        #print ClientAddress
                        if(FirstAddress == ClientAddress):

                                self.clients.remove(client)

                                break
                        else:
                                return
##
##      # This is for the client to be able to send messages.
##        def ClientMessages(self):
##                if (self.clients != []):
##                        for client in self.clients:
##                                Name = client[1]
##                                MessageBody = raw_input(Message)
##                                print  MessageBody
##                                return 4



        # Server has only 1 state that it can be
        def Do_Loop(self):
                try:
                        Open = True
                        SwitchState = 0
                        while Open:
                                if(SwitchState == 0):
                                        SwitchState = self.SendACK()
##                                if(SwitchState == 4):
##                                        SwitchState = self.ClientMessages()
                                else:
                                        print "something went wrong in do_loop server"
                                        break

                except Exception as e:
                        #print e
                        print traceback.format_exc()
                        #print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
