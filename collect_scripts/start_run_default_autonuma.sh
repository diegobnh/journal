#!/bin/bash

source app_dataset.sh

gcc -o lock_memory lock_memory.c

#Autonuma - Default
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}

    sudo -u dmoura mkdir -p ${APP_DATASET[$j]}/autonuma
    sudo -u dmoura chmod +777 ${APP_DATASET[$j]}/autonuma

    cd ${APP_DATASET[$j]}/autonuma
    rm -f *

    cp ../../run.sh .
    cp ../../shared_library/mmap_intercept_only_to_trace.so .

    sudo ./run.sh ${APP[$j]} ${DATASET[$j]} autonuma

    rm run.sh *.so call_stack.txt
    cd ../..
done
