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
        self.data2 = ''


    def Reboot_decorator(func):
        def rebooter(self):
            func(self)
            print(self.data2)
            self.data2 = ''
            time.sleep(5)
            self.reboot()
            return self.data2   
        return rebooter


    def SaR_decorator(func):
        def operations(self):
            func(self)
            self.send_and_rec()
            return self.data2   
        return operations

    def _data_reader(self):
        try:
            data_str = self.data.decode('utf-8')
        except UnicodeDecodeError:
            data_str = self.data.decode('latin-1')
            
        
        # logger.info(f"Decoded response: {data_str}")
        
        data_str = data_str.strip()
        
        try:
            self.data2 = json.loads(data_str)
        except json.JSONDecodeError as e:
            # logger.warning(f"Direct parsing failed: {e}")
            start_idx = data_str.find('{')
            end_idx = data_str.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = data_str[start_idx:end_idx]
                self.data2 = json.loads(json_str)
            else:
                lines = data_str.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('{') and line.endswith('}'):
                        try:
                            self.data2 = json.loads(line)
                            break
                        except json.JSONDecodeError:
                            continue
                else:
                    raise json.JSONDecodeError("No valid JSON data found!", data_str, 0)

        # if "STATUS" in self.data2 and isinstance(self.data2['STATUS'], list):
        #     for i, status in enumerate(self.data2['STATUS']):
        #         if "Code" in status:
                    # logger.info(f"Return Code:{status['Code']}")
                    # assert status['Code'] == (11)
                    # logger.info(f"Decoded response: {self.data2}")
                    # logger.info(f"API call successful! Code is :  {status['Code']}")
                    ...
         
    
    def send_and_rec(self):
        env = {}
        self.data2 = ''
        try:
            env["socket"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            env["socket"].connect(self.server_address)
            # logger.info(f"Connection Openned Successfully to {self.host}")
            env["socket"].sendall(self.msg.encode())  
            time.sleep(1)
            self.data = env["socket"].recv(30000)
            # logger.info(f"Raw response: {self.data}")
            self._data_reader() 
            env["socket"].close()
        except Exception as e:
            logger.warning(f'Connection failed: {e}')
        self.data = ''
        self.msg = ''
        time.sleep(3) 
        # logger.info(f"Connection Closed Successfully to {self.host}") 
        
    @SaR_decorator
    def reboot(self):
        self.msg = '{"command":"reboot"}'  

    
    @SaR_decorator
    def version(self):
        self.msg = '{"command":"version"}'  

    @Reboot_decorator
    @SaR_decorator
    def static(self):
        static_ip = input('Static IP address: ')
        netmask = input('Netmask: ')
        gateway_ip = input('Gateway IP: ')
        dns1 = input('DNS1 Address: ')
        dns2 = input("DNS2 Address: ")
        segment0 = {"dhcp":"0","ip":static_ip,"netmask":netmask,"gateway":gateway_ip,"dns1":dns1,"dns2":dns2}
        segment1 = f'0,network,{segment0}'
        self.msg = {"command":"ascset","parameter":segment1}
        self.msg = str(self.msg)

    @Reboot_decorator
    @SaR_decorator
    def dhcp(self):
        self.msg = '{"command":"ascset","parameter":"0,network,{"dhcp":"1"}"}'  

    @SaR_decorator
    def version(self):
        self.msg = '{"command":"version"}'  


    @SaR_decorator
    def summary(self):
        self.msg = '{"command":"summary"}'  

    @SaR_decorator
    def suspend(self):
        self.msg = '{"command":"ascset","parameter":"0,suspend"}'  
   
    @SaR_decorator
    def restart(self):
        self.msg = '{"command":"restart"}'  

    @SaR_decorator
    def config(self):
        self.msg = '{"command":"config"}'
    
    @SaR_decorator
    def devs(self):
        self.msg = '{"command":"devs"}'
    
    @SaR_decorator
    def pools(self):
        self.msg = '{"command":"pools"}'

    @SaR_decorator
    def devdetails(self):
        self.msg = '{"command":"devdetails"}'

    @SaR_decorator
    def stats(self):
        self.msg = '{"command":"devdetails"}'

    @SaR_decorator
    def stats(self):
        self.msg = '{"command":"coin"}'

    def runall_read(self):
        def sleeper(timer):
            print(f'sleep for {timer}')
            time.sleep(timer)
            
        print(self.version())
        sleeper(20)
        print(self.summary())
        sleeper(20)
        print(self.config())
        sleeper(20)
        print(self.devs())
        sleeper(20)
        print(self.pools())
        sleeper(20)
        print(self.devdetails())
        sleeper(20)
        print(self.stats())
        sleeper(20)
        print(self.coin())
        sleeper(20)
        print(self.reboot())


if __name__ == "__main__":
    IP_addresss = input("Input address of miner: ")
    host = API_Handler(IP_addresss)
    # print(host.suspend())
    # for i in range(0,180,30):
    #     time.sleep(i)
    #     print(f'Pausing for {i} seconds.')
    #     print(host.summary())
    # time.sleep(120)
    # print(host.reboot())

    # print(host.summary())
    # time.sleep(20)
    # print(host.restart())
    # time.sleep(60)
    # print(host.summary())