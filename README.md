# nginx_vts_to_zabbix
Check your Nginx VTS by curl:your_nginx_vts_url #(my_nginx_vts_url http://localhost/statuszone/format/json)
python3 -m pip install requests #(Python library)
Add 2 files from /scripts/ to /etc/zabbix/scripts
In /etc/zabbix/zabbix_agent2.d/ create file userparameter_nginx_vts.conf #(zabbix_agentd.d - if you use zabbix-agent)
Add 2 lines in userparameter_nginx_vts.conf(check mb in your case not python3, but python):
UserParameter=nginx.discovery[*],python3 /etc/zabbix/scripts/nginx-discovery.py $1
UserParameter=nginx.stat[*],python3 /etc/zabbix/scripts/nginx.py $1 $2 $3 $4 $5 $6 $7
systemctl restart zabbix-agent2 #(zabbix-agentd - if you use zabbix-agent)
Check that zabbix-agent gets metrics by commands:
zabbix_agent2 -t nginx.discovery #(zabbix_agentd.d - if you use zabbix-agent)
zabbix_agent2 -t nginx.stat[zone name or nodeIP]  #(zabbix_agentd.d - if you use zabbix-agent)
In zabbix web interface, in Data Collection - Templates, import nginx_vts.xml
