from audioop import add
import socket  
import time
from ipaddress import IPv4Address,IPv4Network
startTime = time.time()

# if __name__ == '__main__':
# target = input('Enter the host to be scanned: ')
# a = gethostbyaddr(gethostname())
# print(a)
# # t_IP = gethostbyname()
# # print ('Starting scan on host: ', a)

# # print(IPv4Address(a))
# addr = str(IPv4Address(a[2][0]))
# print(addr)

# 255.255.255.255
# print(IPv4Address(4294967296-1)) 

a = socket.gethostbyaddr(socket.gethostname())
addr = str(IPv4Address(a[2][0]))
print(addr)
c = addr.split('.')
network_address = str(c[0]+"."+c[1]+"."+c[2]+".")

for i in range(256):
    for j in range(256):
        network_address = str(c[0]+"."+c[1]+"."+str(i)+"."+str(j))
        print(network_address)


# c = addr.split('.')
# print(addr.split('.'))
# network_address = str(c[0]+"."+c[1]+"."+c[2]+".")

# print(network_address)
print('Time taken:', time.time() - startTime)