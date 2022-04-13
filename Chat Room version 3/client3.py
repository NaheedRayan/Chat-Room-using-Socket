# Python program to implement client side of chat room. 
from http import server
from ipaddress import ip_address
import socket 
import select 
import sys 
import threading
from ipaddress import IPv4Address,IPv4Network
import subprocess




import time
startTime = time.time()

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 1: 
	print ("Correct usage: python3 script_name.py") 
	exit() 


# IP_address = str(socket.gethostbyname(socket.gethostname())) 
print("\x1b[1;36;40m{}\x1b[0m {}".format("Scanning for server on port 50000" , ""))
IP_address = ""

# a = socket.gethostbyaddr(socket.gethostname())
# addr = str(IPv4Address(a[2][0]))
# print("Host address 			: " + "\033[1;32m"+addr + '\033[0m')



server_list = []

def check_server(i):
	global server_list

	# IP_address = "192.168.1."+str(i)
	IP_address = i
	Port = int(50000) 

	if(len(server_list)==1):
		# print(IP_address + " Failed")
		return

	else:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

		try:	
			server.connect((IP_address, Port)) 
			# print(IP_address + " Connected")
			print("")
			print("Server IP			: " "\033[1;93m" + IP_address + '\033[0m')
			print("Connection Status		: " "\033[1;93m" + "OK" + '\033[0m')

			server_list.append(server)
			
		except:
			return
			# print(IP_address + " Failed")
			# server.close()


thread_list = []

##############################################################
##############################################################





# Getting the default route adapter name
# ip r | grep "default via " | grep  -E "dev [^ ]*"

cmd = 'ip r | grep "default via " | grep  -Eo "dev [^ ]*"'
ps = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
adapter_name = ps.stdout.decode().strip().split(" ")

print("Adapter name 			: " "\033[1;32m" + adapter_name[1] + '\033[0m')
# print(adapter_name[1]) 



cmd = 'ip r | grep -o "'+ ".*" + adapter_name[1] + " proto kernel" + '"'
ps = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
subnetmask = ps.stdout.decode().strip().split(" ")

# ['192.168.0.0/24', 'dev', 'wlp2s0', 'proto', 'kernel']
# print(subnetmask)

print("Classless address 		: " + "\033[1;32m"+subnetmask[0] + '\033[0m')
ip = subnetmask[0].split("/")
print("Network IP address 		: " + "\033[1;32m"+ip[0] + '\033[0m')
print("Network Mask 			: " + "\033[1;32m"+ip[1] + '\033[0m')


net = IPv4Network(subnetmask[0])
for addr in net:
	# print(addr)
	if(len(server_list) == 1):
		break
	else:
		t1 = threading.Thread(target= check_server,args=(str(addr),))
		thread_list.append(t1)
		t1.start()


##############################################################
##############################################################

# print('Time taken:', time.time() - startTime)
print("Time taken			: " "\033[1;32m" + str(time.time() - startTime) + '\033[0m')
print("")

if(len(server_list)==0):
	print("\033[1;91m" + "No server found" + '\033[0m')
	print("Connection Status		: " "\033[1;91m" + "Failed" + '\033[0m')
	
	sys.exit()


server = server_list[0]

# at the starting it will just send the name

while True:
	# name = ''
	name = input('Enter your name: ')
	if(len(name)<=10 and len(name)!=0):
		server.send(bytes(name , 'utf-8'))
		break
	else :
		print('Length of the name should be less than 11')
		 


# name = ''
# name = input('Enter your name: ')
# server.send(bytes(name , 'utf-8'))

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
