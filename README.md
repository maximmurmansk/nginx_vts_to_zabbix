# nginx_vts_to_zabbix
1. Check your Nginx VTS by `curl:your_nginx_vts_url` #(my_nginx_vts_url: `http://localhost/statuszone/format/json`) <Br>
2. `python3 -m pip install requests` #(Python library) 
3. Add 3 files from /scripts/ to /etc/zabbix/scripts
4. In /etc/zabbix/zabbix_agent2.d/ create file `userparameter_nginx_vts.conf` #(/zabbix_agentd.d/ - if you use zabbix-agent)
5. Add 3 lines in `userparameter_nginx_vts.conf`(check mb in your case not python3, but python):

    ```UserParameter=nginx.discovery[*],python3 /etc/zabbix/scripts/nginx-discovery.py $1```
    ```UserParameter=nginx.stat[*],python3 /etc/zabbix/scripts/nginx-stat.py $1 $2 $3 $4 $5 $6 $7```
    ```UserParameter=nginx.host[*],python3 /etc/zabbix/scripts/nginx-host.py $1 $2 $3 $4 $5 $6 $7```

6. `systemctl restart zabbix-agent2` #(zabbix-agent - if you use zabbix-agent) <Br>
7. Check that zabbix-agent gets metrics by commands: <Br>
`zabbix_agent2 -t nginx.discovery` #(zabbix_agentd - if you use zabbix-agent) <Br>
`zabbix_agent2 -t nginx.stat[zone name or nodeIP]`  #(zabbix_agentd - if you use zabbix-agent) <Br>
`zabbix_agent2 -t nginx.host[host name]`  #(zabbix_agentd - if you use zabbix-agent) <Br>
8. In zabbix web interface, in Data Collection - Templates, import nginx_vts.xml <Br> 

Almost all metrics are in the format like constantly increasing value, but you can change like number of units per minute