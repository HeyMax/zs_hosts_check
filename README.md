# zs_hosts_check  
ZStack物理机状态巡检工具  

## 帮助
    
    #把 xunjian/ 拷贝至管理节点 root/;    
    scp -r xunjian root@192.168.10.110:/root/
    
    #获取帮助
    cd /root/xunjian/ && bash xunjian.sh -h 
    
    #使用
    bash xunjian.sh -p [password] -c [cluster_uuid_1,cluster_uuid_2]
