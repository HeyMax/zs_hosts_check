#!/bin/sh
rm -rf /root/log/
python ./idrsa_asbc.py
ansible-playbook check-host.yaml -i ./ansible.conf
bash zs_check.sh
cd /root/log/
echo ""
grep 警告 /root/log/ -nir
DATE=$(date +%Y%m%d)
cd /root/ && tar -zcvf xunjianlog-${DATE}.tar.gz log > tardetail && rm -rf tardetail && rm -rf log
echo -e "\n巡检结束\n巡检结果存放于：/root/xunjianlog-${DATE}.tar.gz"
echo "delete from SessionVO;"|mysql -u root -pzstack.mysql.password zstack