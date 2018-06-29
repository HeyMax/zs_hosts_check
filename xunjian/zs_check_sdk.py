# -*- coding: UTF-8 -*-
'''
@author: ZhChen

VM operations test 
'''

import apibinding.api_actions as api_actions
import datetime
import time
import os,sys
import zs_api_sdk as zs
import threading
from datetime import datetime,timedelta
reload(sys)
sys.setdefaultencoding('utf8') 
#import queryTest as query

#def_title_10*
def title(str):
	print 28*'#' + str + 28*'#'
	
#def_unit_rec
def unit_rec(num):
	units = {'B':1.0,'KB':1024.0,'MB':1024.0**2,'GB':1024.0**3}
	if num == 0:
		uted_num = '0B'
	else:
		for k,v in sorted(units.items(), key=lambda x:x[1], reverse=True):
			#print k
			if int(int(num)/v) > 0 :
				uted_num = str(round(int(num)/v,2)) + k
				break
	return uted_num
	
#def_query_vm
def query_vm(conditions=[], parameters=[]):
	action = api_actions.QueryVmInstanceAction()
	action.conditions = conditions
	action.parameters = parameters
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt
	
def query_primarystorage(conditions=[], parameters=[]):
	action = api_actions.QueryPrimaryStorageAction()
	action.conditions = conditions 
	action.parameters = parameters
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt 

def query_backupstorage(conditions=[], parameters=[]):
	action = api_actions.QueryBackupStorageAction()
	action.conditions = conditions
	action.parameters = parameters
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt
	
def query_vol(conditions=[], parameters=[]):
	action = api_actions.QueryVolumeAction()
	action.conditions = conditions
	action.parameters = parameters
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt

def query_img(conditions=[], parameters=[]):
	action = api_actions.QueryImageAction()
	action.conditions = conditions
	action.parameters = parameters
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt 
	
def query_host(conditions=[], parameters=[]):
	action = api_actions.QueryHostAction()
	action.conditions = conditions
	action.parameters = parameters
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt
	
def getMetricData(namespace, metricName, labels=[], functions=[]):
	action = api_actions.GetMetricDataAction()
	action.namespace = namespace
	action.metricName = metricName
	action.labels = labels
	action.functions = functions
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt

def getIpAddressCapacity_all(all=True):
	action = api_actions.GetIpAddressCapacityAction()
	action.all = all
	evt = zs.execute_action_with_session(action,zs.login_as_admin())
	return evt

def zs_overview():
	hosts_list = query_host().inventories
	vm_list = query_vm().inventories
	vm_running_list = query_vm(conditions=[{'name':'state','op':'=','value':'Running'}]).inventories
	ps_list = query_primarystorage().inventories
	bs_list = query_backupstorage().inventories
	ipc = getIpAddressCapacity_all()
	title("云平台资源概览")
	amount_hosts = len(hosts_list)
	amount_vm = len(vm_list)
	amount_vm_running = len(vm_running_list)
	amount_ps = len(ps_list)
	amount_bs = len(bs_list)
	
	print '''物理机数量: %d\n云主机数量: %d\n运行中云主机数量: %d\n主存储数量: %d\n镜像服务器数量: %d\nIP地址总量: %s\n可用IP地址量: %s''' % (amount_hosts, amount_vm, amount_vm_running, amount_ps, amount_bs, ipc.totalCapacity, ipc.availableCapacity)
	#Print running_vm information
	overview_information_print("运行中云主机概览", vm_running_list, attrs={'名称':'name', 'uuid':'uuid', 'CPU':'cpuNum', '内存':'memorySize'})
	#Print ps information
	overview_information_print("主存储概览", ps_list, attrs={'名称':'name', 'uuid':'uuid', '可用容量':'availableCapacity', '可用物理容量':'availablePhysicalCapacity'})		
	#Print bs information
	overview_information_print("镜像服务器概览", bs_list, attrs={'名称':'name', 'uuid':'uuid', '可用容量':'availableCapacity'})
	
def overview_information_print(title_str, resource_list, attrs={'名称':'name', 'uuid':'uuid'}):
	if len(resource_list):
		count = 0
		title(title_str)
		for r in resource_list :
			information_line = ""
			for name in attrs.keys():
				information_line = information_line + "%s: %s\t" % (name, r[attrs[name]])
			print "%s.%s" % (str(count+1), information_line)
			count += 1
		return len(resource_list)
	return 0
	
def query_byLastOpDate_vm():
	count = 1
	query_days_num = 90
	base_time = datetime.now() - timedelta(days=query_days_num)
	title("%s天内未操作的云主机" % str(query_days_num))
	
	saf_vm_list = query_vm(conditions=[{'name':'lastOpDate','op':'<=','value':str(base_time)},{'name':'type','op':'=','value':'UserVm'}]).inventories
	if len(saf_vm_list) :
		for vm in saf_vm_list:
			print "%s.名称:%s\tuuid:%s\n  最后操作日期:%s" % (str(count),vm.name,vm.uuid,vm.lastOpDate)
			count += 1
	else:
		print "没有闲置%s天的云主机" % str(query_days_num)
	return len(saf_vm_list)

def query_largestActualSize_vm():
	count = 0
	top = 5
	title("占用物理存储最多的云主机TOP5")
	vm_list = query_vm(conditions=[{'name':'type','op':'=','value':'UserVm'},{'name':'hypervisorType','op':'=','value':'KVM'}]).inventories
	vm_list.sort(cmp=None, key=lambda x:x.allVolumes[0].actualSize, reverse=True)
	if not len(vm_list):
		print "环境中没有云主机"
		return 0
	elif len(vm_list)<5:
		top = len(vm_list)
		while count<top:
			#get_attached_vm
			print "%s.名称:%s\tuuid:%s\n  占用物理容量:%s" % (str(count+1),vm_list[count].name,vm_list[count].uuid,unit_rec(vm_list[count].allVolumes[0].actualSize))
			count += 1
		return vm_list[0].uuid
	
def query_largestActualSize_dv():
	count = 0
	top = 5
	title("占用物理存储最多的云盘TOP5")
	data_volume_list = query_vol(conditions=[{'name':'type','op':'=','value':'Data'},{'name':'format','op':'!=','value':'vmtx'}]).inventories
	data_volume_list.sort(cmp=None, key=lambda x:x.actualSize, reverse=True)
	if not len(data_volume_list):
		print "环境中没有数据云盘"
		return 0
	elif len(data_volume_list)<5:
		top = len(data_volume_list)
		while count<top:
			#largest_actualsize_data_volume
			print "%s.名称:%s\tuuid:%s\n  占用物理容量:%s" % (str(count+1),data_volume_list[count].name,data_volume_list[count].uuid,unit_rec(data_volume_list[count].actualSize))
			count += 1
		return data_volume_list[0].uuid

def query_largestActualSize_topTen_img():
	count = 0
	top = 10
	title("占用物理存储最多的镜像TOP10")
	img_list = query_img(conditions=[{'name':'type','op':'=','value':'zstack'}],parameters=[{'name':'fields','op':'=','value':['uuid','name','actualSize']}]).inventories
	img_list.sort(cmp=None, key=lambda x:x.actualSize, reverse=True)
	if not len(img_list):
		print "环境中没有镜像"
		return 0
	elif len(img_list)<10:
		top = len(img_list)
		while count<top:
			print "%s.名称:%s\tuuid:%s\n  占用物理容量:%s" % (str(count+1),img_list[count].name,img_list[count].uuid,unit_rec(img_list[count].actualSize))
			count += 1
		return len(img_list)
	
def get_cpuOccupancyRateHigh_vm(threshold):
	uservm_list = query_vm(conditions=[{'name':'state','op':'=','value':'Running'},{'name':'type','op':'=','value':'UserVm'},{'name':'hypervisorType','op':'=','value':'KVM'}],parameters=[{'name':'fields','op':'=','value':['uuid','name']}]).inventories
	vm_uuid_name_dict = {}
	vm_uuid_list = []
	for vm in uservm_list:
		vm_uuid_list.append(vm.uuid)
	uservm_uuid_list = '|'.join(vm_uuid_list)
	for vm in uservm_list:
		vm_uuid_name_dict[vm.uuid] = vm.name
	namespace = "ZStack/VM"
	metricName = "CPUAllUsedUtilization"
	cpuOR_list = []
	# def get_vm_cpuload_list(uservm):
		# #get_sorted_cpu_list
		# #for uservm in uservm_list :
		# cpuOR = getMetricData(namespace,metricName,labels=['VMUuid='+uservm.uuid]).data
		# if len(cpuOR):
			# cpuOR_value_avg = (cpuOR[0].value+cpuOR[1].value)/2
			# #print cpuOR_value_avg
			# cpuOR_vm_uuid = cpuOR[0].labels.VMUuid
			# if cpuOR_value_avg >= threshold:
				# cpuOR_list.append({'vm_name':uservm.name,'vm_uuid':cpuOR_vm_uuid,'value_avg':cpuOR_value_avg})
	# #multiThread
	# for i in range(len(uservm_list)):
		# t = threading.Thread(target=get_vm_cpuload_list,args=(uservm_list[i],))
		# t.start()
	vm_data = getMetricData(namespace,metricName,labels=['VMUuid=~'+uservm_uuid_list],functions=['average(groupBy=\"VMUuid\")']).data
	for vm in vm_data:
		if vm.value >= threshold:
			cpuOR_list.append({'vm_name':vm_uuid_name_dict[vm.labels.VMUuid],'vm_uuid':vm.labels.VMUuid,'value_avg':vm.value})
	return cpuOR_list

def print_cpuOccupancyRateHigh_vm(cpuOR_list,threshold):
	title("CPU利用率超过%d%%的云主机" % threshold)
	count = 1
	#get_sorted_cpu_list
	if len(cpuOR_list):
		cpuOR_list.sort(cmp=None, key=lambda x:(x.get('value_avg')), reverse=True)
		#print_saf_vm_list
		for cpuOR in cpuOR_list:
			if cpuOR['value_avg'] >= threshold:
				print "%s.名称:%s	uuid:%s\n  CPU利用率:%.2f%%" % (str(count),cpuOR['vm_name'],cpuOR['vm_uuid'],cpuOR['value_avg'])
				count += 1
			else:
				break
	else:
		print "无CPU利用率超过%d%%的云主机" % threshold

def get_highLoadHosts(threshold_cpu,threshold_mem,threshold_disk):
	host_list = query_host(conditions=[{'name':'status','op':'=','value':'Connected'},{'name':'hypervisorType','op':'=','value':'KVM'}],parameters=[{'name':'fields','op':'=','value':['uuid','name']}]).inventories
	host_uuid_name_dict = {}
	for host in host_list:
		host_uuid_name_dict[host.uuid]=host.name
	namespace = "ZStack/Host"
	metricName_list = ["CPUAllUsedUtilization","MemoryUsedInPercent","DiskAllUsedCapacityInPercent"]
	host_uuid_list = []
	host_cpuhl_list = []
	host_memhl_list = []
	host_diskhl_list = []
	host_cpu = 0
	host_mem = 0
	host_disk = 0
	# def group_hlLoadHosts(host):
		# #for host in host_list:
		# #CPU
		# host_cpu_datas = getMetricData(namespace,metricName_list[0],labels=['HostUuid='+host.uuid]).data
		# if len(host_cpu_datas):
			# host_cpu = (host_cpu_datas[0].value + host_cpu_datas[1].value)/2
		# #MEM
		# host_mem_datas = getMetricData(namespace,metricName_list[1],labels=['HostUuid='+host.uuid]).data
		# if len(host_mem_datas):
			# host_mem = (host_mem_datas[0].value + host_mem_datas[1].value)/2
		# #DISK
		# host_disk_datas = getMetricData(namespace,metricName_list[2],labels=['HostUuid='+host.uuid]).data
		# if len(host_disk_datas):
			# host_disk = (host_disk_datas[0].value + host_disk_datas[1].value)/2
			# #print host_disk
		# host_info = {"host_name":host.name,"host_uuid":host.uuid,"host_cpu":host_cpu,"host_mem":host_mem,"host_disk":host_disk}
		# if host_cpu >= threshold_cpu :
			# host_cpuhl_list.append(host_info)
		# if host_mem >= threshold_mem :
			# host_memhl_list.append(host_info)
		# if host_disk >= threshold_disk :
			# host_diskhl_list.append(host_info)
	# #multiThread
	# for i in range(len(host_list)):
		# t = threading.Thread(target=group_hlLoadHosts,args=(host_list[i],))
		# t.start()
	# if len(host_cpuhl_list):	
		# host_cpuhl_list.sort(cmp=None, key=lambda x:(x.get('host_cpu')), reverse=True)
	# if len(host_memhl_list):
		# host_memhl_list.sort(cmp=None, key=lambda x:(x.get('host_mem')), reverse=True)
	# if len(host_diskhl_list):
		# host_diskhl_list.sort(cmp=None, key=lambda x:(x.get('host_disk')),reverse=True)
	#get hosts_uuid
	for host in host_list:
		host_uuid_list.append(host['uuid'])
	host_uuid_list='|'.join(host_uuid_list)
	#CPU_HL_Hosts
	host_cpu_datas = getMetricData(namespace,metricName_list[0],labels=['HostUuid=~'+host_uuid_list],functions=["average(groupBy=\"HostUuid\")"]).data
	for host in host_cpu_datas:
		if host.value >= threshold_cpu:
			host_cpuhl_list.append({'host_name':host_uuid_name_dict[host.labels.HostUuid],'host_uuid':host.labels.HostUuid,'host_value':host.value})
	#MEM_HL_Hosts
	host_mem_datas = getMetricData(namespace,metricName_list[1],labels=['HostUuid=~'+host_uuid_list],functions=["average(groupBy=\"HostUuid\")"]).data
	for host in host_mem_datas:
		if host.value >= threshold_mem:
			host_memhl_list.append({'host_name':host_uuid_name_dict[host.labels.HostUuid],'host_uuid':host.labels.HostUuid,'host_value':host.value})
	#DISK_HL_Hosts
	host_disk_datas = getMetricData(namespace,metricName_list[2],labels=['HostUuid=~'+host_uuid_list],functions=["average(groupBy=\"HostUuid\")"]).data
	for host in host_disk_datas:
		if host.value >= threshold_disk:
			host_diskhl_list.append({'host_name':host_uuid_name_dict[host.labels.HostUuid],'host_uuid':host.labels.HostUuid,'host_value':host.value})	
	return {'host_cpuhl_list':host_cpuhl_list,'host_memhl_list':host_memhl_list,'host_diskhl_list':host_diskhl_list}

def print_highLoadHosts_list(tc,tm,td,host_cpuhl_list,host_memhl_list,host_diskhl_list):
	#cpu_hl_list
	count = 1
	title("CPU负载高于%d%%的物理机" % tc)
	if len(host_cpuhl_list):
		host_cpuhl_list.sort(cmp=None, key=lambda x:x['host_value'], reverse=True)
		for host in host_cpuhl_list:
			print "%s.名称:%s	uuid:%s\n  CPU利用率:%.2f%%" % (str(count),host['host_name'],host['host_uuid'],host['host_value'])
			count += 1
	else:
		print "无CPU负载超过%d%%的物理机" % tc
	#mem_hl_list
	count = 1
	title("内存负载高于%d%%的物理机" % tm)
	if len(host_memhl_list):
		host_memhl_list.sort(cmp=None, key=lambda x:x['host_value'], reverse=True)
		for host in host_memhl_list:
			print "%s.名称:%s	uuid:%s\n  内存利用率:%.2f%%" % (str(count),host['host_name'],host['host_uuid'],host['host_value'])
			count += 1
	else:
		print "无内存负载高于%d%%的物理机" % tm
	#disk_hl_list
	count = 1
	title("磁盘已用空间高于%d%%的物理机" % td)
	if len(host_diskhl_list):
		host_diskhl_list.sort(cmp=None, key=lambda x:x['host_value'], reverse=True)
		for host in host_diskhl_list:
			print "%s.名称:%s	uuid:%s\n  磁盘已用:%.2f%%" % (str(count),host['host_name'],host['host_uuid'],host['host_value'])
			count += 1
	else:
		print "无磁盘占用超过%d%%的物理机" % td

def print_unattached_datavol_list():
	unAttachedDVList = query_vol(conditions=[{'name':'vmInstanceUuid','op':'is null'},{'name':'type','op':'=','value':'Data'}]).inventories
	count = 1
	title("未加载状态的云盘")
	if len(unAttachedDVList):
		unAttachedDVList.sort(cmp=None, key=lambda x:x.actualSize, reverse=True)
		for dv in unAttachedDVList:
			print "%s.名称:%s\tuuid:%s\n  占用物理容量:%s" % (str(count),dv.name,dv.uuid,unit_rec(dv.actualSize))
			count += 1
	else:
		print "无未加载状态的云盘"

def print_abnormalStateVm_lists():	
	nonRunning_state_vm_list = query_vm(conditions=[{'name':'state','op':'!=','value':'Running'},{'name':'type','op':'=','value':'UserVm'},{'name':'hypervisorType','op':'=','value':'KVM'}]).inventories
	#dict_vm_state
	vm_states={
	'已停止':'Stopped',
	'已暂停':'Paused',
	'启动中':'Starting',
	'停止中':'Stopping',
	'删除中':'Destroying',
	'重启中':'Rebooting'}
	#dict_abnormal_vm_state
	def classify_abnormal_vm(vm_list,states):
		abnormal_state_vm_list = []
		for vm in vm_list:
			if vm.state in states.values():
				abnormal_state_vm_list.append(vm)
		if len(abnormal_state_vm_list):
			abnormal_state_vm_list.sort(cmp=None, key=lambda x:(x.state),reverse=True)
		return abnormal_state_vm_list	
	def print_vm_list_by_state(vm_list):
		count = 0
		title("非运行中云主机")
		if len(vm_list):
			for vm in vm_list:
				print "%s.名称:%s\tuuid:%s\n  状态:%s" % (str(count+1),vm.name,vm.uuid,vm.state)
				count += 1
		else:
			print "所有云主机都在运行中"
	print_vm_list_by_state(classify_abnormal_vm(nonRunning_state_vm_list,vm_states))

def GetDisconnectedPrimaryStorage():
	count = 0
	disconn_PS_list = query_primarystorage(conditions=[{'name':'status','op':'=','value':'Disconnected'}]).inventories
	title("已失联主存储")
	if len(disconn_PS_list):
		for ps in disconn_PS_list:
			print "%s.名称:%s\tuuid:%s" % (str(count+1),ps.name,ps.uuid)
			count += 1
	else:
		print "没有失联主存储"
	return disconn_PS_list

def GetDisconnectedHost():
	count = 0
	disconn_Host_list = query_host(conditions=[{'name':'status','op':'=','value':'Disconnected'}]).inventories
	title("已失联物理机")
	if len(disconn_Host_list):
		for host in disconn_Host_list:
			print "%s.名称:%s\tuuid:%s" % (str(count+1),host.name,host.uuid)
			count += 1
	else:
		print "没有失联物理机"
	return  disconn_Host_list

def GetDisconnectedBackupStorage():
	count = 0
	disconn_BS_list = query_backupstorage(conditions=[{'name':'status','op':'=','value':'Disconnected'},{'name':'__systemTag__','op':'!=','value':'remote'}]).inventories
	title("已失联镜像服务器")
	if len(disconn_BS_list):
		for bs in disconn_BS_list:
			print "%s.名称:%s\tuuid:%s" % (str(count+1),bs.name,bs.uuid)
			count += 1
	else:
		print "没有失联镜像服务器"
	return disconn_BS_list

def GetCapacityShortPrimaryStorage(threshold):
	count = 0
	CS_PS_list = query_primarystorage(conditions=[{'name':'status','op':'=','value':'Connected'}]).inventories
	title("已用物理容量超过%d%%的主存储" % threshold)
	if len(CS_PS_list):
		for ps in CS_PS_list:
			if ps.totalPhysicalCapacity != 0:
				avabPC = (1-round(ps.availablePhysicalCapacity/float(ps.totalPhysicalCapacity),2))*100
				if avabPC > threshold :
					print "%s.名称:%s\tuuid:%s\n  已用物理容量:%s%%" % (str(count+1),ps.name,ps.uuid,str(avabPC))
					count += 1
		if count == 0:
			print "无已用物理容量超过%d%%的主存储" % threshold
	return count

def GetCapacityShortBackupStorage(threshold):
	count = 0
	CS_BS_list = query_backupstorage(conditions=[{'name':'status','op':'=','value':'Connected'},{'name':'__systemTag__','op':'!=','value':'remote'}]).inventories
	title("已用容量超过%d%%的镜像服务器" % threshold)
	if len(CS_BS_list):
		for bs in CS_BS_list:
			if bs.totalCapacity != 0:
				avabPC = (1-round(bs.availableCapacity/float(bs.totalCapacity),2))*100
				if avabPC > threshold:
					print "%s.名称:%s\tuuid:%s\n  已用容量:%s%%" % (str(count+1),bs.name,bs.uuid,str(avabPC))
					count += 1
		if count == 0:
			print "无已用容量超过%d%%的镜像服务器" % threshold
	return count

def CephPSMonsCheck():
	count = 0
	ceph_PS_list = query_primarystorage(conditions=[{'name':'type','op':'=','value':'ceph'}]).inventories
	title("Ceph主存储Mons检查")
	if len(ceph_PS_list):
		for ps in ceph_PS_list:
			print "%s.名称:%s\tuuid:%s" % (str(count+1),ps.name,ps.uuid)
			disconn_mon = 0
			count += 1
			for mon in ps.mons:
				if mon['status'] == 'Disconnected':
					disconn_mon += 1
					print "  Warning:%s已失联" % mon['monAddr']
			if disconn_mon == 0:
				print "  所有Mon节点连接正常"
	else:
		print "没有Ceph类型主存储"