# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import _thread
# from thread import *



"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit()
else:
    print(f'{sys.argv[0]} running') 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 

# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 

""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 

list_of_clients = [] 
def clientthread(conn, addr): 

	# sends a message to the client whose user object is conn 
	# conn.send(bytes("Welcome to this chatroom!", 'utf-8')) 

	# since its a thread then each user will have a different name 
	# receiving connection from the client and receiveing the name
	name = ''
	name = conn.recv(2048).decode()
	
	
	# welcoming the client and broadcasting clients connection to other users
	msg = "({}){} {}".format(addr[0] , name , 'is connected.')
	msg = "{:*^70}".format(msg)
	print(msg)	
	broadcast(msg , conn)

	# here the main conversation starts
	while True: 
			try: 
				message = conn.recv(2048).decode() 
				if message: 

					"""prints the ip , name and message of the 
					user who just sent the message on the server 
					terminal"""
					
					# message_to_send = "({})({:-^20}) {}".format(addr[0] , name , message)
					# sending colored message
					# ip is yellow color
					ip = '\x1b[1;33;40m' + str(addr[0]) + '\x1b[0m'
					# name is red text on white background
					name1 ="\x1b[1;31;40m{:-^20}\x1b[0m".format(name)
					# green text
					msg = '\x1b[1;32;40m' + message + '\x1b[0m'
					

					# formatting the message and printing and broadcasting it
					message_to_send = "({})({}) {}".format(ip , name1 , msg)
					print(message_to_send)
					broadcast(message_to_send, conn) 

				else: 
					"""message may have no content if the connection 
					is broken, in this case we remove the connection and close it"""
					msg = "({}){} {}".format(addr[0] , name , 'left the chat.')
					msg = "{:*^70}".format(msg)
					
					print(msg)
					broadcast(msg , conn)

					# removing the connection and closing it
					conn.close()
					remove(conn) 

			except: 
				continue

"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(bytes(message, 'utf-8')) 
			except:

				msg = "({}){} {}".format(addr[0] , name , 'not available.')
				msg = "{:*^70}".format(msg) 
				print(msg)
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients) 

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
	if connection in list_of_clients: 
		list_of_clients.remove(connection) 

while True: 

	"""Accepts a connection request and stores two parameters, 
	conn which is a socket object for that user, and addr 
	which contains the IP address of the client that just 
	connected"""
	conn, addr = server.accept() 

	"""Maintains a list of clients for ease of broadcasting 
	a message to all available people in the chatroom"""
	list_of_clients.append(conn) 

	# prints the address of the user that just connected 
	print (addr[0] + " connected") 

	# creates and individual thread for every user 
	# that connects 
	_thread.start_new_thread(clientthread,(conn,addr))
    # start_new_thread(clientthread,(conn,addr)) 

conn.close() 
server.close() 
