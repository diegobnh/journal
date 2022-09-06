#!/bin/bash

source app_dataset.sh

for ((i = 0; i < ${#TYPES_OF_MEM_PRESSU[@]}; i++)); do
	for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
        echo "Running:"${APP_DATASET[$j]}" for memory pressure:"${TYPES_OF_MEM_PRESSU[$i]} 

        if [[ ${TYPES_OF_MEM_PRESSU[$i]} == "30" ]]; then
            folder_name="autonuma_30"
        elif [[ ${TYPES_OF_MEM_PRESSU[$i]} == "50" ]]; then
            folder_name="autonuma_50"
        else
            folder_name="autonuma_70"
        fi

        cd ${APP_DATASET[$j]}/$folder_name

        cp ../../post_process.sh .
	    sudo ./post_process.sh ${APP[$j]} ${APP_DATASET[$j]} > /dev/null 2>&1
	    rm post_process.sh

        cp ../../mmap_break_to_chunks.py .
        python3 mmap_break_to_chunks.py
        rm mmap_break_to_chunks.py

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
