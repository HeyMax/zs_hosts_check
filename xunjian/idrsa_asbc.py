import os

#get_host_ips_str
host_ip_list = os.popen('echo "select managementIp from HostVO where hypervisorType = \'KVM\';"| mysql -u root -pzstack.mysql.password zstack|grep -v managementIp').read()
host_ips = host_ip_list.split("\n")[:-1]

#get_host_usernames_str
host_username_list = os.popen('echo "select username,password from KVMHostVO;"| mysql -u root -pzstack.mysql.password zstack|grep -v username').read()
host_usernames_list = host_username_list.split("\n")
host_usernames = []
for host_username in host_usernames_list:
	host_usernames.append(host_username.split("\t"))
host_usernames = host_usernames[:-1]
#same_len
if len(host_usernames) < len(host_ips):
	Dvalue = len(host_ips) - len(host_usernames)
	while Dvalue > 0:
		host_usernames.append(["",""])
		Dvalue -= 1

#create_kv_username_password
count = 0
userpassword_kvs = []
while count < len(host_ips):
	userpassword_kvs.append("".join(host_ips[count]+" ansible_ssh_user=" + host_usernames[count][0] + " ansible_ssh_private_key_file=/usr/local/zstack/apache-tomcat/webapps/zstack/WEB-INF/classes/ansible/rsaKeys/id_rsa" ))
	count += 1
kvs_str = "\n".join(userpassword_kvs)

file_asbc = open('ansible.conf','w')
file_asbc.write(kvs_str)
file_asbc.close()
