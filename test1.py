from audioop import add
from socket import *
import time

from ipaddress import IPv4Address,IPv4Network
startTime = time.time()

# if __name__ == '__main__':
# target = input('Enter the host to be scanned: ')
a = gethostbyaddr(gethostname())
# t_IP = gethostbyname()
# print ('Starting scan on host: ', a)
addr = str(IPv4Address(a[2][0]))
c = addr.split('.')
# print(addr.split('.'))
network_address = str(c[0]+"."+c[1]+"."+c[2]+".")

print(network_address)
print('Time taken:', time.time() - startTime)