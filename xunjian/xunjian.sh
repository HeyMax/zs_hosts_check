#!/bin/sh
python ./idrsa_asbc.py
rm -rf /root/log/
ansible-playbook check-host.yaml -i ./ansible.conf
bash zs_check.sh
echo "巡检结束"
cd /root/log/
echo "巡检结果存放于：/root/log/"
grep 警告 /root/log/ -nir
echo "delete from SessionVO;"|mysql -u root -pzstack.mysql.password zstack
