#!/bin/bash

source app_dataset.sh

for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}

    cd ${APP_DATASET[$j]}/autonuma
    python3 ../../generate_static_mapping.py
    cd ../..
done
