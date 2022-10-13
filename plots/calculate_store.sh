#!/bin/bash

source APP_DATASET.sh
: '
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

        python3 -W ignore ../../calculate_store.py > intersection_store.csv

        cd ../..
    done
done
'
grep dram */autonuma_70/intersection_store.csv | awk -F, '{print $N1}'  | awk -F/ '{print $1}' > app_dataset

grep pmem */autonuma_30/intersection_store.csv | awk -F, '{print $NF}' | tr -d " " > store_30_pmem
grep pmem */autonuma_50/intersection_store.csv | awk -F, '{print $NF}' | tr -d " " > store_50_pmem
grep pmem */autonuma_70/intersection_store.csv | awk -F, '{print $NF}' | tr -d " " > store_70_pmem

grep dram */autonuma_30/intersection_store.csv | awk -F, '{print $NF}' | tr -d " " > store_30_dram
grep dram */autonuma_50/intersection_store.csv | awk -F, '{print $NF}' | tr -d " " > store_50_dram
grep dram */autonuma_70/intersection_store.csv | awk -F, '{print $NF}' | tr -d " " > store_70_dram

paste app_dataset store_30_dram store_50_dram store_70_dram store_30_pmem store_50_pmem store_70_pmem -d, > store_ratio.csv

rm -f app_dataset store_30_* store_50_* store_70_*

python3 plot_store_ratio.py
