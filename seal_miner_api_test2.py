import requests
import json
import socket

def apiconnect(IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    data = "Failure"
    
    try:
        sock.connect((IP, 4028))
        payload = {"command":"ascset",
                   "parameter":"0,suspend"}

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
    L3 = apiconnect("10.17.1.1")
    print(L3)
    L3 = L3[:-1]
    print(L3)
    result = json.loads(L3)
    print(result)
     #   print("")
      #  print(i)