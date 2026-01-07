# coding:utf-8
# test sealminer 4028 API

import json
import logging
import socket 
import time 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration: Replace with your miner's IP and port
host = "172.16.100.216"
server_address = (host, 4028)

env = {}

def data_reader(data):
    try:
        data_str = data.decode('utf-8')
        print("UTF")
    except UnicodeDecodeError:
        data_str = data.decode('latin-1')
        print("UTF")
    
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
                # assert status['Code'] == (22)

                logger.info(f"API call successful! Code is :  {status['Code']}")
    return data2

def send_and_rec(msg):
    env["socket"].sendall(msg.encode())  
    time.sleep(1)
    return env["socket"].recv(30000)  

def test_reboot():
    message = '{"command":"reboot"}'  
    data = send_and_rec(message)
    logger.info(f"Raw response: {data}")
    data_reader(data)

def test_static():
    message = '{"command":"ascset","parameter":"0,network,{"dhcp":"0","ip":"10.17.3.2","netmask":"255.255.255.0","gateway":"10.17.3.254","dns1":"8.8.8.8","dns2":"114.114.114.114"}"}'  
    data = send_and_rec(message)
    logger.info(f"Raw response: {data}")
    data_reader(data)
    time.sleep(3)
    test_reboot()

def test_dhcp():
    message = '{"command":"ascset","parameter":"0,network,{"dhcp":"1"}"}'  
    data = send_and_rec(message)
    logger.info(f"Raw response: {data}")
    data_reader(data)
    time.sleep(3)
    test_reboot()

def test_version():
    message = '{"command":"version"}'  
    data = send_and_rec(message)
    logger.info(f"Raw response: {data}")
    data_reader(data)


def test_summary():
    message = '{"command":"summary"}'  
    data = send_and_rec(message)
    logger.info(f"Raw response: {data}")
    data_reader(data)


def test_suspend():
    message = '{"command":"ascset","parameter":"0,suspend"}'  
    data = send_and_rec(message)
    logger.info(f"Suspend API Raw response: {data}")

def test_restart():
    message = '{"command":"restart"}'  
    data = send_and_rec(message)
    logger.info(f"Restart API Raw response: {data}")

    data2 = data_reader(data)
    
    if "id" in data2:
        logger.info(f"Return id:{data2['id']}")
        assert data2['id'] == (1)
        logger.info(f"Restart API call successful! id is : {data2['id']}")

def test():
    env["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    env["socket"].connect(server_address)

    # test_version()
    test_summary()
    
    # test_suspend()
    # test_restart()

    env["socket"].close()

if __name__ == "__main__":
    test()