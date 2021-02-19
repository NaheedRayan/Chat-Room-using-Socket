# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print ("Correct usage: script, IP address, port number") 
	exit() 


IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 

# at the starting it will just send the name
name = ''
name = input('Enter your name: ')
server.send(bytes(name , 'utf-8'))



def recv_msg(conn):
    while 1:
        try:
            message = conn.recv(2048).decode('utf-8') 
            print (message) 
        except :
            # if the connection is broken
            print('Connection Broken')
            conn.close()
            quit()

def send_msg(conn):
    while 1:
            
        message = input() 

        # if the user wants to quit
        if message == 'QUIT':
            conn.close()
            quit()

        # for blue text	
        print("\x1b[1;36;40m{}\x1b[0m {}".format(" You " , message))
        conn.send(bytes(message , 'utf-8'))

try:

    t1 = threading.Thread(target=recv_msg , args=(server,))
    t2 = threading.Thread(target=send_msg , args=(server,))


    t1.start()
    t2.start()

    t1.join()
    t2.join()
    # _thread.start_new_thread(recv_msg , (server , ))
    # _thread.start_new_thread(send_msg , (server , ))
except:
    print('Something went wrong')
    server.close()


server.close() 
