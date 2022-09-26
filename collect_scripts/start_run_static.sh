#!/bin/bash

source app_dataset.sh


sudo -u dmoura ./generate_static_mapping.sh


sudo -u dmoura mkdir -p  static_results
sudo -u dmoura chmod +777 static_results

cd static_results
sudo rm -rf * exec_time_*

for ((i = 0; i < ${#TYPES_OF_MEM_PRESSURE[@]}; i++)); do
    for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
        if [[ ${TYPES_OF_MEM_PRESSURE[$i]} == "30" ]]; then
            mem_press=${MEM_PRESSURE_30[$j]}
            cp ../${APP_DATASET[$j]}/autonuma/"static_mapping_30.txt" static_mapping.txt
            #cp static_mapping_30.txt static_mapping.txt
        elif [[ ${TYPES_OF_MEM_PRESSURE[$i]} == "50" ]]; then
            mem_press=${MEM_PRESSURE_50[$j]}
            cp ../${APP_DATASET[$j]}/autonuma/"static_mapping_50.txt" static_mapping.txt
            #cp static_mapping_30.txt static_mapping.txt
        else
            mem_press=${MEM_PRESSURE_70[$j]}
            cp ../${APP_DATASET[$j]}/autonuma/"static_mapping_70.txt" static_mapping.txt
            #cp static_mapping_30.txt static_mapping.txt
        fi
        echo "Collecting Static Mapping:"${APP_DATASET[$j]}, " Memory Pressure of "${TYPES_OF_MEM_PRESSURE[$i]}
  	    cp ../shared_library/mmap_intercept_to_static_bind.so .

        numactl --membind=0 .././lock_memory $mem_press &
        lock_memory_pid=$!
        sleep 5

        start=`date +%s`
    	sudo .././run.sh ${APP[$j]} ${DATASET[$j]} static_mapping

        end=`date +%s`
        exec_time=$(echo $start $end | awk '{printf "%.2f", ($2-$1)/60}')
        echo ${APP_DATASET[$j]},$exec_time >> exec_time_${TYPES_OF_MEM_PRESSURE[$i]}

        kill -10 $lock_memory_pid

        mkdir -p ${APP_DATASET[$j]}_${TYPES_OF_MEM_PRESSURE[$i]}
        mv static_mapping.txt static_out_*.csv track_info_${APP_DATASET[$j]}.csv ${APP_DATASET[$j]}_${TYPES_OF_MEM_PRESSURE[$i]}
        rm -f call_stack.txt perf.data
        sleep 10
    done
done
