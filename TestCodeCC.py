# Test code

#For sevrer
ServerC = centreChat.ChatServer(port)
thread.start_new_thread(ServerC.handleMessages())

Accum = []

#for client
ClientC = centreChat.ChatClient("127.0.0.1", port, "Meow")
thread.start_new_thread(ClientC.handleMessages())
# add "Meow" to list

ClientC1 = centreChat.ChatClient(" ", port, 'Yo')
thread.start_new_thread(Client1.handleMessages())
#add yo to list

ClientC2 = centreChat.ChatClient(" ", 'loser')
thread.start_new_thread(ClientC2.handleMessage())
#add loser to list

time.sleep(1)

for eachname in Accum:
    list2 = S.getClient()
    num = list2.find(eachname)
if num == -1:
    print "nope"
    



