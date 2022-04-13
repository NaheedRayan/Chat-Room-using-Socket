
import subprocess
from ipaddress import IPv4Address
from ipaddress import IPv4Network
import socket



# Getting the default route adapter name
# ip r | grep "default via " | grep  -E "dev [^ ]*"

cmd = 'ip r | grep "default via " | grep  -Eo "dev [^ ]*"'
ps = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
adapter_name = ps.stdout.decode().strip().split(" ")

print("Adapter name         : " "\033[1;32m" + adapter_name[1] + '\033[0m')
# print(adapter_name[1]) 



hostname = socket.gethostname()
print("Hostname             : " + "\033[1;32m"+hostname + '\033[0m')

local_ip = socket.gethostbyname(hostname)
print("local ip             : " + "\033[1;32m"+local_ip + '\033[0m')




cmd = 'ip r | grep -o "'+ ".*" + adapter_name[1] + " proto kernel" + '"'
ps = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
subnetmask = ps.stdout.decode().strip().split(" ")

# ['192.168.0.0/24', 'dev', 'wlp2s0', 'proto', 'kernel']
# print(subnetmask)

print("Classless address    : " + "\033[1;32m"+subnetmask[0] + '\033[0m')
ip = subnetmask[0].split("/")
print("Network IP address   : " + "\033[1;32m"+ip[0] + '\033[0m')
print("Network Mask         : " + "\033[1;32m"+ip[1] + '\033[0m')


# net = IPv4Network(subnetmask[0])
# for addr in net:
#     print(addr)
