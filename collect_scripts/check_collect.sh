#!/bin/bash

source app_dataset.sh

for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do

    cd ${APP_DATASET[$j]}/autonuma

    columns=$(grep mmap allocations_${APP_DATASET[$j]}.csv | head | awk -F',' '{print NF; exit}')
    if [[ $columns -ne 6 ]]; then
       echo -n ${APP_DATASET[$j]}
       echo " missing column!"
    fi

    cd ../..
done

