# -*- coding: UTF-8 -*-
'''
@author: ZhChen

This script is used to test the basic operations of VM
'''

import apibinding.api_actions as api_actions
import time
import hashlib
import os,sys
import zs_api_sdk as zs
#import queryTest as query
import zs_check_sdk as check
import datetime
#exec
if __name__ == "__main__":
	#Hosts_thresholds
	htc = 80
	htm = 80
	htd = 80
	#HLHostsLists
	hl_hosts_lists = check.get_highLoadHosts(htc,htm,htd)
	cpu_hl_hosts_list = hl_hosts_lists['host_cpuhl_list']
	mem_hl_hosts_list = hl_hosts_lists['host_memhl_list']
	disk_hl_hosts_list = hl_hosts_lists['host_diskhl_list']
	#cpuHL_Vm_List
	vtc = 80
	cpu_hl_vm_list = check.get_cpuOccupancyRateHigh_vm(vtc)
	#datetime
	datetime = datetime.datetime.now()
	os.system('clear')
	print "############################ 管理节点巡检 ############################"
	print "巡检日期:%s" % datetime
	
	#Resources OverView
	check.zs_overview()
	time.sleep(10)
	os.system('clear')
	
	#QueryByLastOpDate_VM
	resultDateQueryVm = check.query_byLastOpDate_vm()
	time.sleep(10)
	os.system('clear')
	
	#LargestActualSize_VM
	resultLargestActualSizeVm = check.query_largestActualSize_vm()
	#time.sleep(10)
	#os.system('clear')
	
	#LargestActualSize_DataVolume
	resultLargestActualSizeDataVolume = check.query_largestActualSize_dv()
	#time.sleep(5)
	#os.system('clear')
	
	#LargestActualSize_Image_Top10
	resultLargestActualSizeImageTop10 = check.query_largestActualSize_topTen_img()
	time.sleep(10)
	os.system('clear')
	
	#cpuOccupancyRateHigh_vm
	resultGetCpuOccupancyRateHighVm = check.print_cpuOccupancyRateHigh_vm(cpu_hl_vm_list,vtc)
	time.sleep(10)
	os.system('clear')
	
	#printHighLoadHostsList
	resultPrintThemAll = check.print_highLoadHosts_list(htc,htm,htd,cpu_hl_hosts_list,mem_hl_hosts_list,disk_hl_hosts_list)
	time.sleep(10)
	os.system('clear')
	
	#printUnAttachedDataVolumes
	resultPrintUnAttachedDataVolumes = check.print_unattached_datavol_list()
	time.sleep(10)
	os.system('clear')
	
	#printAvailableCapacityShortPS/BS
	CSPS = 80
	CSBS = 80
	resultGetCapacityShortPrimaryStorage = check.GetCapacityShortPrimaryStorage(CSPS)
	resultGetCapacityShortBackupStorage = check.GetCapacityShortBackupStorage(CSBS)
	time.sleep(10)
	os.system('clear')
	
	#printDisconnectedPS
	resultGetDisconnectedHost = check.GetDisconnectedHost()
	resultGetDisconnectedPrimaryStorage = check.GetDisconnectedPrimaryStorage()
	resultGetDisconnectedBackupStorage = check.GetDisconnectedBackupStorage()
	time.sleep(10)
	os.system('clear')
	
	#CephPSCheck
	resultCephPSMonsCheck = check.CephPSMonsCheck()
	time.sleep(10)
	os.system('clear')
	
	#print_abnomalStateVm_lists
	resultPrintABVMAll = check.print_abnormalStateVm_lists()	
	#done
	#print "\n管理节点巡检完成\n管理节点巡检结果存放于：/root/log/MN_log"
