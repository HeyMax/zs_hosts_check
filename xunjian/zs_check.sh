#!/bin/bash
if ! [ -s /root/log/MN_log ]
then
    touch /root/log/MN_log
fi
    
#bak the original log.py as log.py.bak
cp -f /var/lib/zstack/virtualenv/zstackcli/lib/python2.7/site-packages/zstacklib/utils/log.py ./log.py.bak
#replace it with ./log.py 
cp -f ./log.py /var/lib/zstack/virtualenv/zstackcli/lib/python2.7/site-packages/zstacklib/utils/log.py

#new log.py detail
#ch = logging.StreamHandler(logfd) -> fh = logging.FileHandler
#ch.setLevel(logging.DEBUG) -> fh.setLevel(logging.DEBUG)
#ch.setFormatter(formatter) -> fh.setFormatter(formatter)
#logger.addHandler(ch) -> logger.addHandler(fh)
#/var/lib/zstack/virtualenv/zstackcli/lib/python2.7/site-packages/zstacklib/utils/

source /var/lib/zstack/virtualenv/zstackcli/bin/activate
export ZS_SERVER_IP=$1

#cat /ZSPySDK.2.2/VMTEST_README

python -u ./zs_check.py | tee -a /root/log/MN_log
sed -i 's/\x1b\[3;J\x1b\[H\x1b\[2J//' /root/log/MN_log
#recover log.py
mv -f ./log.py.bak /var/lib/zstack/virtualenv/zstackcli/lib/python2.7/site-packages/zstacklib/utils/log.py