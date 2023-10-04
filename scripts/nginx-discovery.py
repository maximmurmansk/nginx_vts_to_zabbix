import json
import sys
import os
import re
import requests

# Parse JSON from nginx to dict data
url = "http://localhost/statuszone/format/json"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("Error retrieving or parsing JSON:", str(e))
    sys.exit(1)

# Forming JSON for Zabbix LLD where {#UPSTREAM} - upstream's name
# {#NODE_IP} - peer's IP address
result = []

# Find server zones
for i in sorted(data['serverZones'].keys()):
    if str(i) == "*":
        continue
    result.append({"{#ZONE}": str(i)})

# Find upstream zones, if none, exit
try:
    'server' in sorted(data['upstreamZones'].keys())
except KeyError as e:
    pass
else:
    for i in sorted(data['upstreamZones'].keys()):
        ip_data = dict([[v['server'], v] for v in data['upstreamZones'][i]])
        for j in sorted(ip_data.keys()):
            result.append({
                "{#UPSTREAM}": str(i),
                "{#NODE_IP}": str(j)
            })

print(json.dumps(result))