#!/bin/bash
DUMP_NODE_IP=$1
DUMP_NODE_PSWD=$2
usage(){
  echo -e "Usage: bash $0 [dump_node_ip] [dump_node_password]\nSuch as: bash $0 192.168.123.123 password"
  exit 77
}

export_crontab(){
  crontab -l > /tmp/crontab.bak
}

remove_crontabfile(){
  rm -f /tmp/crontab.bak
}

crontab_dump(){
  if [ -e "/tmp/crontab.bak" ]
  then
    if
      grep ".* zstack-ctl dump_mysql  --host root@$DUMP_NODE_IP --d --keep-amount .*" /tmp/crontab.bak
      then
        echo "管理节点已在$DUMP_NODE_IP上备份"
      else
        sshpass -p $DUMP_NODE_PSWD ssh-copy-id $DUMP_NODE_IP -o StrictHostKeyChecking=no
        echo "30 */2 * * * zstack-ctl dump_mysql  --host root@$DUMP_NODE_IP --d --keep-amount 24" >> /tmp/crontab.bak | crontab /tmp/crontab.bak; rm -f /tmp/crontab.bak && crontab -l
    fi
  fi
}

main(){
  if [ $# != 2 ]
  then
    usage
  fi
  export_crontab
  crontab_dump
  remove_crontabfile
}

main $DUMP_NODE_IP $DUMP_NODE_PSWD
#if [ $# != 2 ]
#then
#  usage
#fi
#export_crontab
#crontab_dump
#remove_crontabfile
