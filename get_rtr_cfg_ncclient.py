'''
Open a NC connection with your IOS-XR router and retrieve ths config in XML
'''
from ncclient import manager
import configparser

'''
Have an INI file with your router configuration
testbed.ini example is
  [edge100.local]
  Host = 212.143.181.142
  SSHPort = 22
  NCPort = 830
  UserName = router_username
  Password = router_password
'''

config = configparser.ConfigParser()
config.read('/path/to/file/testbed.ini')
device=config['edge100.local']

netconf_connection = manager.connect(host=device['Host'], 
                                     port=device['NCPort'],
                                     username=device['UserName'],
                                     password=device['Password'],
                                     hostkey_verify=False,
                                     device_params={'name':'iosxr'})

response = netconf_connection.get_config(source='running')
print(response)
