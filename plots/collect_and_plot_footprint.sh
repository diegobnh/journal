#!/bin/bash

source app_dataset.sh

#Autonuma - Default
mkdir -p temp
cd ..
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}

    cd ${APP_DATASET[$j]}/autonuma

    python3 ../../plots/post_process_mem_footprint.py "track_info_"${APP_DATASET[$j]}".csv"
    mv *_footprint.csv ../../plots/temp
    
    cd ../..
done

cd plots
cat temp/*.csv > temp/all_app_avg_footprint.csv
python3 plot_mem_footprint.py temp/all_app_avg_footprint.csv

mv temp/*.pdf .
rm -r temp
