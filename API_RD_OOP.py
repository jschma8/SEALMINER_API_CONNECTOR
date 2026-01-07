# coding:utf-8
# test sealminer 4028 API

import json
import logging
import socket 
import time 




# Setup Logging for better exception handling

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("API_OOP.log", mode="a", encoding="utf-8")
logger.addHandler(console_handler)
logger.addHandler(file_handler)
formatter = logging.Formatter(
   "{asctime} - {levelname} - {message}",
    style="{",
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
# Class initializaion
class API_Handler():
    def __init__(self, host):
        self.host = host
        self.server_address = (self.host, 4028)
        self.data = ''
        self.msg = ''

    def _data_reader(self):
        try:
            data_str = self.data.decode('utf-8')
        except UnicodeDecodeError:
            data_str = self.data.decode('latin-1')
            
        
        logger.info(f"Decoded response: {data_str}")
        
        data_str = data_str.strip()
        
        try:
            data2 = json.loads(data_str)
        except json.JSONDecodeError as e:
            # logger.warning(f"Direct parsing failed: {e}")
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
                    # logger.info(f"Return Code:{status['Code']}")
                    # assert status['Code'] == (11)
                    logger.info(f"Decoded response: {data2}")
                    logger.info(f"API call successful! Code is :  {status['Code']}")
        return

    def send_and_rec(self):
        env = {}
        env["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        env["socket"].connect(self.server_address)
        logger.info(f"Connection Openned Successfully to {self.host}")
        env["socket"].sendall(self.msg.encode())  
        time.sleep(1)
        self.data = env["socket"].recv(30000)
        # logger.info(f"Raw response: {self.data}")
        self._data_reader() 
        env["socket"].close()
        self.data = ''
        self.msg = ''
        time.sleep(3) 
        logger.info(f"Connection Closed Successfully to {self.host}") 
    
    def reboot(self):
        self.msg = '{"command":"reboot"}'  
        self.send_and_rec()

    
    def version(self):
        self.msg = '{"command":"version"}'  
        self.send_and_rec()  

    def static(self):
        self.msg = '{"command":"ascset","parameter":"0,network,{"dhcp":"0","ip":"10.17.3.2","netmask":"255.255.255.0","gateway":"10.17.3.254","dns1":"8.8.8.8","dns2":"114.114.114.114"}"}'  
        self.send_and_rec()
        time.sleep(3)
        self.reboot()

    def dhcp(self):
        self.msg = '{"command":"ascset","parameter":"0,network,{"dhcp":"1"}"}'  
        self.send_and_rec()
        time.sleep(3)
        self.reboot()

    def version(self):
        self.msg = '{"command":"version"}'  
        self.send_and_rec()


    def summary(self):
        self.msg = '{"command":"summary"}'  
        self.send_and_rec()


    def suspend(self):
        self.msg = '{"command":"ascset","parameter":"0,suspend"}'  
        self.send_and_rec()

    def restart(self):
        self.msg = '{"command":"restart"}'  
        self.send_and_rec()

if __name__ == "__main__":
    host = API_Handler('172.16.100.216')
    host.version()
    time.sleep(5)
    host.summary()