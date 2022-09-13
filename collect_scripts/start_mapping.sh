#!/bin/bash

source app_dataset.sh

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

        python3 -W ignore ../../mapping.py $(pwd)

        cd ../..
    done
done
