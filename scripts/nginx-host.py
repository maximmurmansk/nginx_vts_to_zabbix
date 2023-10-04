import json
import sys
import requests

# Replace with your NGINX status URL
nginx_status_url = "http://localhost:82/statuszone/format/json"

# Function to fetch NGINX status data
def fetch_nginx_status(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error retrieving or parsing JSON:", str(e))
        sys.exit(1)

# Function to format JSON for Zabbix with specified metrics
def format_zabbix_json(data):
    metrics = {}

    if data:
        desired_metrics = [
            "nginxVersion",
            "loadMsec",
            "nowMsec",
            "connections"
        ]

        for metric in desired_metrics:
            if metric in data:
                metrics[metric] = data[metric]

    return metrics

# Fetch NGINX status data
nginx_status_data = fetch_nginx_status(nginx_status_url)

# Format data for Zabbix with specified metrics
zabbix_json = format_zabbix_json(nginx_status_data)

# Print the JSON for Zabbix
if zabbix_json:
    zabbix_json["connections"] = {
        "active": 0,
        "reading": 0,
        "writing": 0,
        "waiting": 0,
        "accepted": 0,
        "handled": 0,
        "requests": 0
    }
    if "connections" in nginx_status_data:
        zabbix_json["connections"] = nginx_status_data["connections"]

    print(json.dumps(zabbix_json))
else:
    print("No desired metrics found.")