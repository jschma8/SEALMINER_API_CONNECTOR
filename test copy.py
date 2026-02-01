import pandas as pd
import numpy as np

static_ip = input('Static IP address: ')
netmask = input('Netmask: ')
gateway_ip = input('Gateway IP: ')
dns1 = input('DNS1 Address: ')
dns2 = input("DNS2 Address: ")
segment0 = {"dhcp":"0","ip":static_ip,"netmask":netmask,"gateway":gateway_ip,"dns1":dns1,"dns2":dns2}
segment1 = f'0,network,{segment0}'
msg = {"command":"ascset","parameter":segment1}
msg = str(msg)
