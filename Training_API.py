# This is a test script for SEALMiner API

import json
import logging
import socket
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def api(IP):
    server_address = (IP, 4028)

    env = {}

    env["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    env["socket"].connect(server_address)

    message = '{"command":"version"}'

    env["socket"].sendall(message.encode())
    time.sleep(1)
    data = env["socket"].recv(30000)
    
    try:
        data_str = data.decode("utf-8")
    except UnicodeDecodeError:
        data_str = data.decode("latin-1")
    
    data_str = data_str.strip()

    try:
        data2 = json.loads(data_str)
    except json.JSONDecodeError as e:
        
        logger.warning(f"Direct Parsing failed: {e}")

        start_idx = data_str.find("{")
        end_idx = data_str.rfind("}")+1

        if start_idx != -1 and end_idx != 0: 
            json_str = data_str[start_idx:end_idx]
            data2 = json.loads(json_str)
        else:
            lines = data_str.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        data2 = json.loads(line)
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                raise json.JSONDecodeError("No valid JSON data found", data_str,0)
    
    print(data2)

    env["socket"].close()

if __name__ == "__main__":
    host = "172.16.15.65"
    api(host)