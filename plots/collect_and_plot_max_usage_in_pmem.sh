#!/bin/bash

source ../APP_DATASET.sh

rm -f max_pmem_*.csv

for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    cd ../${APP_DATASET[$j]}/autonuma

    max_pmem=$(cat track_info* | awk -F"," 'NR>1{print $3}' | datamash max 1)
    if [ "$max_pmem" -eq "0" ]; then
        max_pmem=1;
    fi

    echo $max_pmem >> ../../plots/"max_pmem_default.csv"
    cd ../../plots
done

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

	cd ../${APP_DATASET[$j]}/$folder_name

        max_pmem=$(cat track_info* | awk -F"," 'NR>1{print $3}' | datamash max 1)
        if [ "$max_pmem" -eq "0" ]; then
           max_pmem=1;
        fi

        echo $max_pmem >> ../../plots/"max_pmem_"${TYPES_OF_MEM_PRESSURE[$i]}".csv"

        cd ../../plots
    done
done


rm -f app_dataset.csv
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo ${APP_DATASET[$j]} >> app_dataset.csv
done

paste app_dataset.csv max_pmem_default.csv max_pmem_30.csv max_pmem_50.csv max_pmem_70.csv -d , > max_pmem.csv
rm -f add_dataset.csv
rm -f max_pmem_*.csv

python3 plot_max_usage_in_pmem.py
