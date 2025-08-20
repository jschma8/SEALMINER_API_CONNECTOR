import socket
import json
import pandas as pd

def apiconnect(IP, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    data = "Failure"
    
    try:
        sock.connect((IP, 4028))
        payload = {"command":unicode(command}
        sock.send(bytes(json.dumps(payload),'utf-8'))
        data = sock.recv(1024)
    except Exception as e:
        data = e
    finally:
        sock.close()
    return data 

if __name__ == '__main__':
    # df = pd.read_csv("file/fil.csv")
    # ips = df['IP'].to_list()
    # print(ips[25])
    # # for i in range(5090):
    # #     result = apiconnect("10.17.1.1","version")
    # #     print(result)
