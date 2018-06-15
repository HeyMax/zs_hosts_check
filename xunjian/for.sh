#!/bin/bash
function getdir(){
    for element in `ls $1`
    do
        dir_or_file=$1"/"$element
        if [ -d $dir_or_file ]
        then
            getdir $dir_or_file
        else
            grep '#* virsh list(Running&Paused) #*' $dir_or_file -A1000|grep '#* qemu-kvm进程namelist #*' -B1000|grep -o '[0-9a-z]\{32\}';
        fi
    done
}
root_dir="."
getdir $root_dir
