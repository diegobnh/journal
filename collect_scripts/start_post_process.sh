#!/bin/bash

source app_dataset.sh

for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}
    
    cd ${APP_DATASET[$j]}/autonuma
    sudo ../../post_process.sh ${APP[$j]} ${APP_DATASET[$j]} > /dev/null 2>&1
    #python3 ../../mmap_break_to_chunks.py
    #python3 ../../munmap_break_to_chunks.py
	
    cd ../..
done

for ((i = 0; i < ${#TYPES_OF_MEM_PRESSURE[@]}; i++)); do
    for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
        echo "Running:"${APP_DATASET[$j]}" for memory pressure:"${TYPES_OF_MEM_PRESSURE[$i]} 

        if [[ ${TYPES_OF_MEM_PRESSURE[$i]} == "30" ]]; then
            folder_name="autonuma_30"
        elif [[ ${TYPES_OF_MEM_PRESSURE[$i]} == "50" ]]; then
            folder_name="autonuma_50"
        else
            folder_name="autonuma_70"
        fi

        cd ${APP_DATASET[$j]}/$folder_name

	sudo ../../post_process.sh ${APP[$j]} ${APP_DATASET[$j]} > /dev/null 2>&1
        #python3 ../../mmap_break_to_chunks.py
        #python3 ../../munmap_break_to_chunks.py

        cd ../..
    done
done


: '
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}

    cd ${APP_DATASET[$j]}/static_mapping
    cp ../../post_process.sh .

    sudo ./post_process.sh ${APP[$j]} ${APP_DATASET[$j]} > /dev/null 2>&1

    rm post_process.sh run.sh *.so
    cd ../..
done
'
