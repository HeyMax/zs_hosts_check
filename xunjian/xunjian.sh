#!/bin/sh
LOG_PATH=root

usage(){
	echo "Usage: bash $0 -p [MN_admin_password]"
	exit 77
}

sudo python ssh_info.py

while getopts "p:a:" opt;
do
	case $opt in
	  p )
             sudo sed -i "s/^user_password = .*/user_password = \'$OPTARG\'/g" zs_api_sdk.py
	     ;;
	  
	  c )
             sudo python ./ssh_info.py $OPTARG
             ;;
		 
	  * )
	     usage
	     ;;
	esac
done

sudo rm -rf /$LOG_PATH/log/
DATE_START=$(date +%s)
sudo ansible-playbook check-host.yaml -i ./ansible.conf
sudo bash zs_check.sh
DATE_FINISH=$(date +%s)
RUN_TIME=$(($DATE_FINISH-$DATE_START))
sudo cd /$LOG_PATH/log/
echo -e "\n############################ 物理机警告信息 ############################\n$(grep 警告 /$LOG_PATH/log/ -nir|grep -v "物理机警告信息")"|tee -a /$LOG_PATH/log/MN_log
DATE=$(date +%Y%m%d)
sudo echo -e "\n本次巡检用时"$RUN_TIME"秒" >> /$LOG_PATH/log/MN_log
echo -e "管理节点备份任务:\n$(sudo crontab -l | grep ".* zstack-ctl dump_mysql  --host root@.* --d --keep-amount .*")" >> /$LOG_PATH/log/MN_log 
cd /$LOG_PATH/ && sudo tar -zcvf xunjianlog-${DATE}.tar.gz log > tardetail && sudo rm -rf tardetail && sudo rm -rf log
echo -e "\n巡检结束\n巡检结果存放于：/$LOG_PATH/xunjianlog-${DATE}.tar.gz"
echo "delete from SessionVO;"|mysql -u root -pzstack.mysql.password zstack
echo 用时"$RUN_TIME"秒
