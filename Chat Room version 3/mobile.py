# Python program to implement client side of chat room. 
from http import server
from ipaddress import ip_address
import socket 
import select 
import sys 
import threading
from ipaddress import IPv4Address,IPv4Network




import time
startTime = time.time()

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 2: 
	print ("Correct usage: python3 script_name.py IP_addresss") 
	exit() 


# IP_address = str(socket.gethostbyname(socket.gethostname())) 
print("\x1b[1;36;40m{}\x1b[0m {}".format("Scanning for server on port 50000" , ""))
IP_address = ""

# a = socket.gethostbyaddr(socket.gethostname())
a = sys.argv[1]
# addr = str(IPv4Address(a[2][0]))
c = a.split('.')
network_address = str(c[0]+"."+c[1]+"."+c[2]+".")



server_list = []

def check_server(i):

	global server_list

	# if(len(server_list)==1):
	# 	return
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

	# IP_address = "192.168.1."+str(i)
	IP_address = network_address+str(i)
	Port = int(50000) 

	
	try:	
		server.connect((IP_address, Port)) 
		print(IP_address + " Connected")
		server_list.append(server)
 
	
	except:
		print(IP_address + " Failed")
		 

		# server.close()


thread_list = []

for i in range(255):
	if(len(server_list) == 1):
		break
	else:
		t1 = threading.Thread(target= check_server,args=(i,))
		thread_list.append(t1)
		t1.start()


for thread in thread_list:
	thread.join()

print('Time taken:', time.time() - startTime)

if(len(server_list)==0):
	print("No server found")
	exit()


server = server_list[0]

# at the starting it will just send the name
name = ''
name = input('Enter your name: ')
server.send(bytes(name , 'utf-8'))

while True: 

	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 

	""" 
	There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true.
	Note it does not work in Windows because select cant use socket and stdin
	in the same thread."""
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

	for socks in read_sockets: 
		if socks == server: 
			message = socks.recv(2048).decode('utf-8') 
			print (message) 
		else: 
		
			message = input() 

			# if the user wants to quit
			if message == 'QUIT':
				server.close()

			# for blue text	
			# print("\x1b[1;36;40m{}\x1b[0m {}".format(" You " , message))
			server.send(bytes(message , 'utf-8'))
			
server.close() 
