#!/bin/sh
usage(){
	echo "Usage: bash $0 -p [MN_admin_password]"
	exit 77
}

python ./idrsa_asbc.py

while getopts "p:a:" opt;
do
	case $opt in
	  p )
	     sed -i "s/^user_password = .*/user_password = \'$OPTARG\'/g" zs_api_sdk.py
	     ;;
	  
	  a )
		 sed -i "s/$/& ansible_ssh_port=$OPTARG/g" ansible.conf
		 ;;
		 
	  * )
	     usage
	     ;;
	esac
done


rm -rf /root/log/
DATE_START=$(date +%s)
ansible-playbook check-host.yaml -i ./ansible.conf
bash zs_check.sh
DATE_FINISH=$(date +%s)
RUN_TIME=$(($DATE_FINISH-$DATE_START))
cd /root/log/
echo -e "\n############################ 物理机警告信息 ############################\n$(grep 警告 /root/log/ -nir)"|tee -a /root/log/MN_log
DATE=$(date +%Y%m%d)
echo -e "\n本次巡检用时"$RUN_TIME"秒" >> /root/log/MN_log
cd /root/ && tar -zcvf xunjianlog-${DATE}.tar.gz log > tardetail && rm -rf tardetail && rm -rf log
echo -e "\n巡检结束\n巡检结果存放于：/root/xunjianlog-${DATE}.tar.gz"
echo "delete from SessionVO;"|mysql -u root -pzstack.mysql.password zstack
echo 用时"$RUN_TIME"秒