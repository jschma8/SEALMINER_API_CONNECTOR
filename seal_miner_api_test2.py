import requests
import json
import socket

def apiconnect(IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    data = "Failure1"
    
    try:
        sock.connect((IP, 4028))
        payload = {"command":"ascset",
                   "parameter":"0,suspend"}

        sock.send(bytes(json.dumps(payload),'utf-8'))
        data = sock.recv(8192)
        data = json.loads(data[:-1])
    except Exception as e:
        data = e
    finally:
        sock.close()
    return data

if __name__ == '__main__':
    # df = pd.read_csv("file/fil.csv")
    # ips = df['IP'].to_list()
    # print(ips[25])
    # L3 = apiconnect("10.17.1.1")
    # print(L3)

     #   print("")
      #  print(i)
    result =  {'STATUS': [{'STATUS': 'S', 'When': 1755726832, 'Code': 119, 'Msg': 'ASC 0 set OK', 'Description': 'bdminer 4.11.1'}], 'id': 1}
    print(result["STATUS"][0]['Code'])