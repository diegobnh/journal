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

: '
#Autonuma with Memory Pressure
for ((i = 0; i < ${#TYPES_OF_MEM_PRESSURE[@]}; i++)); do
    for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
        if [[ ${TYPES_OF_MEM_PRESSURE[$i]} == "30" ]]; then
	    folder_name="autonuma_30"
            mem_press=${MEM_PRESSURE_30[$j]}
        elif [[ ${TYPES_OF_MEM_PRESSURE[$i]} == "50" ]]; then
            folder_name="autonuma_50"
            mem_press=${MEM_PRESSURE_50[$j]}
        else
            folder_name="autonuma_70"
            mem_press=${MEM_PRESSURE_70[$j]}
        fi
        echo "Running:"${APP_DATASET[$j]}, "Memory Pressure of "${MEM_PRESSURE[$i]}

        sudo -u dmoura mkdir -p ${APP_DATASET[$j]}
	sudo -u dmoura mkdir -p ${APP_DATASET[$j]}/$folder_name
	sudo -u dmoura chmod +777 ${APP_DATASET[$j]}/$folder_name

	cd ${APP_DATASET[$j]}/$folder_name
	rm -f *

	cp ../../run.sh .
	cp ../../shared_library/mmap_intercept_only_to_trace.so .

        numactl --membind=0 ../.././lock_memory $mem_press &
        lock_memory_pid=$!

	sudo ./run.sh ${APP[$j]} ${DATASET[$j]} autonuma

        #kill -9 $python_pid 1> /dev/null  2> /dev/null
        kill -10 $lock_memory_pid

	rm run.sh *.so call_stack.txt
	cd ../..
        sleep 10
    done
done
'

: '
#Static Mapping
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}

    sudo -u dmoura mkdir -p ${APP_DATASET[$j]}/static_mapping
    sudo -u dmoura chmod +777 ${APP_DATASET[$j]}/static_mapping

    cd ${APP_DATASET[$j]}/static_mapping
    rm -f *

    cp ../../run.sh .
    cp ../../shared_library/mmap_intercept_to_static_bind.so .

    sudo ./run.sh ${APP[$j]} ${DATASET[$j]} static_mapping

    rm run.sh *.so call_stack.txt
    cd ../..
done
'
