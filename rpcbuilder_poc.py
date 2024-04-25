from ncclient import manager
import configparser

'''
Using a short list for POC
'''
data= [
      {'prefix': '10.0.0.0/16', 'exact': False, 'greater-equal': 8}, 
      {'prefix': '5.181.156.0/22', 'exact': True}, 
      {'prefix': '5.59.244.0/22', 'exact': False, 'less-equal': 24}, 
      {'prefix': '5.181.156.0/22', 'exact': False, 'greater-equal': 24, 'less-equal': 24}
      ]

def rpcpayload(data):
    #PREFIX-LIST NAME SHOULD BE AUTOMATED and not Hard Coded
    prefix_set_name="AS-TEST"
  
    #RPC Prefix
    payload = f"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
<routing-policy xmlns="http://openconfig.net/yang/routing-policy">
 <defined-sets>
  <prefix-sets>
   <prefix-set>
    <config>
     <name>{prefix_set_name}</name>
     #MODE should not be Hard Coded
     <mode>IPV4</mode>
    </config>
    <name>{prefix_set_name}</name>
    <prefixes>
"""
    #For every prefix in the list run test and place in the RPC Structure
  
    for prefix in (data):
    #CHECK IF LAST (N) ITERATION IN THE DICTIONARY, IF It does avoid the new line after finishes, and add the RPC suffix
        if (data[-1]) == prefix:
            #IF EXACT MATCH FOR LAST ITERATION
            if(prefix['exact'] is True):
                payload += f"     <prefix>\n"
                payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                payload += f"      <config>\n"
                payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                payload += f"       <masklength-range>exact</masklength-range>\n"
                payload += f"      </config>\n"
                payload += f"      <masklength-range>exact</masklength-range>\n"
                payload += f"     </prefix>"
                payload += """
    </prefixes>
   </prefix-set>
  </prefix-sets>
 </defined-sets>
</routing-policy>
</config>
"""
            else:
                #IF LE & GE MATCH FOR LAST ITERATION
                if('less-equal' in prefix and 'greater-equal' in prefix):
                    payload += f"     <prefix>\n"
                    payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                    payload += f"      <config>\n"
                    payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                    payload += f"       <masklength-range>{prefix['less-equal']}..{prefix['greater-equal']}</masklength-range>\n"
                    payload += f"      </config>\n"
                    payload += f"      <masklength-range>{prefix['less-equal']}..{prefix['greater-equal']}</masklength-range>\n"
                    payload += f"     </prefix>"
                    payload += """
    </prefixes>
   </prefix-set>
  </prefix-sets>
 </defined-sets>
</routing-policy>
</config>
"""
                else:
                    #IF ONLY LE MATCH FOR LAST ITERATION
                    if ('less-equal' in prefix):
                        payload += f"     <prefix>\n"
                        payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      <config>\n"
                        payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"       <masklength-range>{prefix['prefix'][-2:]}..{prefix['less-equal']}</masklength-range>\n"
                        payload += f"        <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      </config>\n"
                        payload += f"      <masklength-range>{prefix['prefix'][-2:]}..{prefix['less-equal']}</masklength-range>\n"
                        payload += f"     </prefix>"
                        payload += """
    </prefixes>
   </prefix-set>
  </prefix-sets>
 </defined-sets>
</routing-policy>
</config>
"""
                    #IF ONLY GE MATCH FOR LAST ITERATION
                    else:
                        payload += f"     <prefix>\n"
                        payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      <config>\n"
                        payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"       <masklength-range>{prefix['greater-equal']}..32</masklength-range>\n"
                        payload += f"        <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      </config>\n"
                        payload += f"      <masklength-range>{prefix['greater-equal']}..32</masklength-range>\n"
                        payload += f"     </prefix>"
                        payload += """
    </prefixes>
   </prefix-set>
  </prefix-sets>
 </defined-sets>
</routing-policy>
</config>
"""
        #Start with 0 to N-1 Iteration
        else:
            if(prefix['exact'] is True):
                payload += f"     <prefix>\n"
                payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                payload += f"      <config>\n"
                payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                payload += f"       <masklength-range>exact</masklength-range>\n"
                payload += f"      </config>\n"
                payload += f"      <masklength-range>exact</masklength-range>\n"
                payload += f"     </prefix>\n"
            else:
                if('less-equal' in prefix and 'greater-equal' in prefix):
                    payload += f"     <prefix>\n"
                    payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                    payload += f"      <config>\n"
                    payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                    payload += f"       <masklength-range>{prefix['less-equal']}..{prefix['greater-equal']}</masklength-range>\n"
                    payload += f"      </config>\n"
                    payload += f"      <masklength-range>{prefix['less-equal']}..{prefix['greater-equal']}</masklength-range>\n"
                    payload += f"     </prefix>\n"
                else:
                    if ('less-equal' in prefix):
                        payload += f"     <prefix>\n"
                        payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      <config>\n"
                        payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"       <masklength-range>{prefix['prefix'][-2:]}..{prefix['less-equal']}</masklength-range>\n"
                        payload += f"        <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      </config>\n"
                        payload += f"      <masklength-range>{prefix['prefix'][-2:]}..{prefix['less-equal']}</masklength-range>\n"
                        payload += f"     </prefix>\n"
                    else:
                        payload += f"     <prefix>\n"
                        payload += f"      <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      <config>\n"
                        payload += f"       <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"       <masklength-range>{prefix['greater-equal']}..32</masklength-range>\n"
                        payload += f"        <ip-prefix>{prefix['prefix']}</ip-prefix>\n"
                        payload += f"      </config>\n"
                        payload += f"      <masklength-range>{prefix['greater-equal']}..32</masklength-range>\n"
                        payload += f"     </prefix>\n"
                        
    #Print only for Debug Purposes
    '''
    print(payload)
    '''
    return (payload)


'''
Send to Router via Netconf
'''

config = configparser.ConfigParser()
config.read('/path/to/ini/testbed.ini')
device=config['edge100.local']

netconf_connection = manager.connect(host=device['Host'], 
                                     port=device['NCPort'],
                                     username=device['UserName'],
                                     password=device['Password'],
                                     hostkey_verify=False,
                                     device_params={'name':'iosxr'})

response = netconf_connection.edit_config(config=rpcpayload(data), target="candidate")
response = netconf_connection.commit()

print(response)
