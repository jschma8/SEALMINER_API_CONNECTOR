# coding:utf-8
# test sealminer 4028 API

import json
import logging
import socket 
import time 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration: Replace with your miner's IP and port
host = "172.18.74.162"
server_address = (host, 4028)

env = {}

def send_and_rec(msg):
    env["socket"].sendall(msg.encode())  
    time.sleep(1)
    return env["socket"].recv(30000)  




def test():
    env["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    env["socket"].connect(server_address)

    message = '{"command":"version"}'  
    data = send_and_rec(message)
    logger.info(f"Raw response: {data}")

    try:
        data_str = data.decode('utf-8')
    except UnicodeDecodeError:
        data_str = data.decode('latin-1')
    
    logger.info(f"Decoded response: {data_str}")
    
    data_str = data_str.strip()
    
    try:
        data2 = json.loads(data_str)
    except json.JSONDecodeError as e:
        logger.warning(f"Direct parsing failed: {e}")
        start_idx = data_str.find('{')
        end_idx = data_str.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            json_str = data_str[start_idx:end_idx]
            data2 = json.loads(json_str)
        else:
            lines = data_str.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    try:
                        data2 = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                raise json.JSONDecodeError("No valid JSON data found!", data_str, 0)

    if "STATUS" in data2 and isinstance(data2['STATUS'], list):
        for i, status in enumerate(data2['STATUS']):
            if "Code" in status:
                logger.info(f"Return Code:{status['Code']}")
                assert status['Code'] == (22)

                logger.info(f"API call successful! Code is :  {status['Code']}")


    env["socket"].close()

if __name__ == "__main__":
    test()