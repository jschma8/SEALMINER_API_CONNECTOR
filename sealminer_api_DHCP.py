import json
import socket
import time

def apiconnect(IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    data = "Failure"
    
    try:
        sock.connect((IP, 4028))
#  This is the command that will need to be changed to required information. 
        payload = '{"command":"ascset","parameter":"0,network,{"dhcp":"1"}"}'

        sock.send(bytes(json.dumps(payload),'utf-8'))
        data = sock.recv(30000)
        data = json.loads(data[:-1])
    except Exception as e:
        data = e
    finally:
        sock.close()
# Substitute for return print.
    print(data)
# Implement change
    reboot_data = reboot(IP)
    return reboot_data



def reboot(IP):
    time.sleep(5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    internal_data = "Failure"

# This will implement the change. 
    try:
        sock.connect((IP, 4028))
        payload = {"command":"reboot"}
        sock.send(bytes(json.dumps(payload),'utf-8'))
        internal_data = sock.recv(1024)
        internal_data = json.loads(internal_data[:-1])
    except Exception as e:
        internal_data = e
    finally:
        sock.close()

    return internal_data 

if __name__ == '__main__':
# Verified works on Firmware 1024  2025-11-25

# Change IP to IP being modified
    IP = "XX.XX.XX.XX"
    sealminer = apiconnect(IP)
    print(sealminer)


# 50:D4:48:4B:78:17