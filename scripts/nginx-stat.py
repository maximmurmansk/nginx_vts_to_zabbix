import json
import requests
import sys

# Replace with your NGINX status URL
nginx_status_url = "http://localhost:82/statuszone/format/json"

# Replace with the desired zone or upstream (e.g., "app.whatcrm.net" or "my_upstream")
name_to_fetch = sys.argv[1]

# Function to fetch NGINX status data
def fetch_nginx_status(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error retrieving or parsing JSON:", str(e))
        sys.exit(1)

# Function to format JSON for Zabbix with metrics for a specific zone or upstream
def format_zabbix_json(data, name):
    metrics = {}
    values = {}  # Initialize values to an empty dictionary

    if data:
        if name in data['serverZones']:
            values = data['serverZones'][name]
        elif 'upstreamZones' in data:
            for upstream_name, upstream_data in data['upstreamZones'].items():
                for peer_data in upstream_data:
                    if peer_data['server'] == name:
                        values = peer_data
                        metrics["{#UPSTREAM}"] = upstream_name
                        break
                if "Values" in locals():
                    break

        metrics["{#NAME}"] = name
        metrics["Requests"] = values.get('requestCounter', 0)
        metrics["BytesIn"] = values.get('inBytes', 0)
        metrics["BytesOut"] = values.get('outBytes', 0)
        metrics["ActiveConnections"] = values.get('activeConnections', 0)

        # Include responses data if available
        responses = values.get('responses', {})
        for key, value in responses.items():
            metrics["Responses_%s" % key] = value

        return json.dumps(metrics)

# Fetch NGINX status data
nginx_status_data = fetch_nginx_status(nginx_status_url)

# Format data for Zabbix with metrics for the specified zone or upstream
zabbix_json = format_zabbix_json(nginx_status_data, name_to_fetch)

# Print the JSON for Zabbix
if zabbix_json:
    print(zabbix_json)
else:
    print("Invalid zone or upstream name.")