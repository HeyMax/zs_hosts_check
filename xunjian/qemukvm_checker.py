#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import re
from collections import Counter

mysql_list = os.popen('''echo "select state,uuid from VmInstanceVO where hypervisorType='KVM';" | mysql -uroot -pzstack.mysql.password zstack | egrep "Running|Paused"''').read()
mysql_list = re.sub(r'Running|Paused', "", mysql_list).split()
virsh_list = os.popen('cd /root/log/ && bash /root/xunjian/for.sh').read().split()
qemukvm_list = os.popen("cd /root/log/ && grep '#* qemu-kvm进程namelist #*' . -nir -A1000|grep '[0-9a-z]\{32\}'").read()
qemukvm_list = re.sub(r'\.\/|H(.*)[-,:](\d)*[-,:]|(.*-name)|(.*qemu-kvm)|(--)', "", qemukvm_list).split()
qemukvm_kvl = {}

for item in qemukvm_list:
	item_kv = item.split('/')
	if item_kv[1] in qemukvm_kvl.values():
		qemukvm_kvl[item_kv[1]] = qemukvm_kvl[item_kv[1]].appen(item_kv[0])
	qemukvm_kvl[item_kv[1]] = [item_kv[0]]

#qemukvm_kvl['b09c58af3963403297c1f0b4eb96beb1'].append('172.20.131.124')	
qemukvm_list = qemukvm_kvl.keys()
list_dup=list(set(mysql_list)&set(qemukvm_list))

# print mysql_list
#print virsh_list
# print qemukvm_list
# print qemukvm_kvl

# print len(mysql_list)
# print len(qemukvm_kvl)
# print len(qemukvm_list)

# print list_dup
# print len(list_dup)

# if len(mysql_list) >= len (qemukvm_list):
	# list_diff = list(set(mysql_list)-set(qemukvm_list))
# else:
	# list_diff = list(set(qemukvm_list)-set(mysql_list))

# print list_diff
# print len(list_diff)
	
def qemukvm_cmp(list1,list2,cmp_list):
	if len(list1) >= len (list2):
		list_diff = list(set(list1)-set(list2))
	else:
		list_diff = list(set(list2)-set(list1))
	if list_diff == []:
		print "物理机上qemu-kvm进程信息与{}信息一致\n\n".format(cmp_list)
		return 0
	else:
		print "物理机上qemu-kvm进程信息与{}信息不同,异常uuid如下:".format(cmp_list)
		try:	
			for uuid in list_diff:
				print "UUID:{}\t所在Host:{}".format(uuid, qemukvm_kvl[uuid])
		except KeyError:
			for uuid in list_diff:
				print uuid
			print "{}信息与qemu-kvm进程信息不匹配,请重新巡检以更新xunjianlog\n\n".format(cmp_list)
		return 1

def dupliacate_qemukvm_checking(qemukvm_list):
	count = 0
	for name in qemukvm_list:
		if len(qemukvm_kvl[name]) > 1 :
			print "警告:重名虚拟机进程:{}\t所在Hosts:{}".format(name, str(qemukvm_kvl[name]))
			count += 1
	if not count:
		print "没有重名虚拟机进程"
		return 0
	return count

if __name__ == '__main__':
	print '\n\n'+28*'#'+'ZSDB云主机信息&虚拟机进程匹配检查'+28*'#'
	qemukvm_cmp(mysql_list, qemukvm_list, "数据库")
	print '\n\n'+28*'#'+'virsh-list信息&虚拟机进程匹配检查'+28*'#'
	qemukvm_cmp(virsh_list, qemukvm_list, "virshlist")
	print '\n\n'+28*'#'+'重名虚拟机进程检查'+28*'#'
	dupliacate_qemukvm_checking(qemukvm_list)
