# -*- coding: UTF-8 -*-
'''
@author: ZhChen

Time synchronization checker
'''
import os,sys,re

ntp_state = os.popen('systemctl list-units --type=service --state=running --no-pager | grep ".service"|grep ntpd.service').read()
chrony_state = os.popen('systemctl list-units --type=service --state=running --no-pager | grep ".service"|grep chronyd.service').read()

host_ntp_servers = re.sub(r'\.\/|\/H(.*)[-,:](\d)*[-,:]| *LOCAL.*', "", os.popen('cd /root/log/ && grep "^\*[0-9]" . -nir|grep -v "MN_log"').read()).split('\n')[:-2]
host_ntp_servers_kv = {}

host_chrony_servers = re.sub(r'\.\/|\/H(.*)[-,:](\d)*[-,:]', "", os.popen('cd /root/log/ && grep "^\^[*,+,-,?,x,~]" . -nir|grep -v "MN_log"').read()).split('\n')
host_chrony_servers_kv = {}


if ntp_state :
    print "\n############################ MN NTP时间服务检查 ############################"
    print "MN NTP服务运行中\n"
    print os.popen('ntpq -np').read()
elif chrony_state:
    print "\n############################ MN Chrony时间服务检查 ############################"
    print "MN Chrony服务运行中\n"
    print os.popen('chronyc sources').read()
else:
    print "MN NTP&Chrony服务都未运行"


print "\n############################ 物理机NTP服务检查 ############################"
if len(host_ntp_servers):
	for index in range(0, len(host_ntp_servers)):
		host_ntp_servers_kv[host_ntp_servers[index].split('*')[0]] = host_ntp_servers[index].split('*')[1]
		print host_ntp_servers[index].split('*')[0] + ' NTPServer: ' + host_ntp_servers[index].split('*')[1].split('     ')[0]	

print "\n############################ 物理机Chrony服务检查 ############################"
if len(host_chrony_servers) - 1:
	for index in range(0, len(host_chrony_servers)-1):
		print host_chrony_servers[index].split("                      ", 1)[0]
