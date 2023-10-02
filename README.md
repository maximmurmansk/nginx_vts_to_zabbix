# nginx_vts_to_zabbix
Check your Nginx VTS by curl:your_nginx_vts_url #(my_nginx_vts_url http://localhost/statuszone/format/json) <Br>
python3 -m pip install requests #(Python library) <Br>
Add 2 files from /scripts/ to /etc/zabbix/scripts <Br>
In /etc/zabbix/zabbix_agent2.d/ create file userparameter_nginx_vts.conf #(zabbix_agentd.d - if you use zabbix-agent) <Br>
Add 2 lines in userparameter_nginx_vts.conf(check mb in your case not python3, but python): <Br>
UserParameter=nginx.discovery[*],python3 /etc/zabbix/scripts/nginx-discovery.py $1 <Br>
UserParameter=nginx.stat[*],python3 /etc/zabbix/scripts/nginx.py $1 $2 $3 $4 $5 $6 $7 <Br>
systemctl restart zabbix-agent2 #(zabbix-agentd - if you use zabbix-agent) <Br>
Check that zabbix-agent gets metrics by commands: <Br>
zabbix_agent2 -t nginx.discovery #(zabbix_agentd.d - if you use zabbix-agent) <Br>
zabbix_agent2 -t nginx.stat[zone name or nodeIP]  #(zabbix_agentd.d - if you use zabbix-agent) <Br>
In zabbix web interface, in Data Collection - Templates, import nginx_vts.xml <Br> 
