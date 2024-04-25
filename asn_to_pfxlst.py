'''
This code was introduced by Renato Almeida de Oliveira in his Tutorial here
https://www.youtube.com/watch?v=rOnIfPZUgiY
'''

import requests
import json
import subprocess

def get_as_set(asn):
    request = requests.get(
            "https://www.peeringdb.com/api/net?asn=" + str(asn))
    request.raise_for_status()
    response = json.loads(request.text)
    return response['data'][0]['irr_as_set']

#Test get_as_set Procedure by querying peeringdb AS109, expected result is CISCO AS-SET (AS-CISCO)
'''
print(get_as_set(109))
'''

def get_as_set_prefixes(as_set, ip_version, aggregate=None):
    args = ["bgpq4", "-j"]
    if(ip_version == 4 or ip_version == 6):
        args.append("-" + str(ip_version))
    else:
        raise Exception("Incorrect IP version")
    if(aggregate):
        args.append("-A")
    args.append("-lirr_prefix")
    args.append(as_set)
    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(process.returncode != 0):
        raise Exception(f"BGPq4 failed:\n{str(process.stderr)}")
    output = json.loads(process.stdout) 
    return output['irr_prefix']

#Test proecedure by quering ASN49791 prefixes by AS-SET
'''
data = get_as_set_prefixes(get_as_set(49791),4,aggregate=True)
print(data)
'''
