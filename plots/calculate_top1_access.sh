#!/bin/bash

source APP_DATASET.sh
rm -f top1_nvm*

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

        value=$(cat sorted_obj_by_metric.csv | awk -F, 'NR>1{print $2}' | datamash max 1)
        echo $value >> ../../top1_nvm_${TYPES_OF_MEM_PRESSURE[$i]}

        cd ../..
    done
done

grep dram */autonuma_70/intersection_store.csv | awk -F, '{print $N1}'  | awk -F/ '{print $1}' > app_dataset
paste app_dataset top1_nvm_30 top1_nvm_50 top1_nvm_70 -d, > top1_access_nvm.csv
python3 plot_top1_nvm.py
rm -f top1_nvm*
