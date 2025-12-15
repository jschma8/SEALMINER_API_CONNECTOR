import requests
import json
import socket
import time

def apiconnect(IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    data = "Failure"
    
    try:
        with open('packet.json', 'r') as file:
            data = json.load(file)
            print(data)
        sock.connect((IP, 4028))
        payload = data
        # payload = {"command":"pools"}
        payload = {"command":"ascset",
                  "parameter":"0,network,{\"dhcp\":\"0\",\"ip\":\"10.17.3.1\",\"netmask\":\"255.255.255.0\",\"gateway\":\"10.17.3.254\",\"dns1\":\"8.8.8.8\",\"dns2\":\"8.8.8.8\"}"}
    #    payload = {"command":"ascset",
    #               "parameter":"0,workmode,{\"mode\":\"normal\"}"}
    #     payload = {"command":"reboot"}
        sock.send(bytes(json.dumps(payload),'utf-8'))
        data = sock.recv(1024)
        data = json.loads(data[:-1])
    except Exception as e:
        data = e
    finally:
        sock.close()
    return data 

if __name__ == '__main__':

    #for i in range(5090):
    L3 = apiconnect("10.17.3.6")
    print(L3)

     #   print("")
      #  print(i)
