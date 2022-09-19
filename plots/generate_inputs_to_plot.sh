#!/bin/bash

source app_dataset.sh

rm -f input_perc_access_DRAM_and_PMEM.csv 
rm -f app_dataset.csv

for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
 
    ram=$(grep Ram ${APP_DATASET[$j]}/autonuma_30/summary_load_access_${APP_DATASET[$j]}.csv | awk -F, '{print $2}')
    pmem=$(grep PMEM ${APP_DATASET[$j]}/autonuma_30/summary_load_access_${APP_DATASET[$j]}.csv | awk -F, '{print $2}')
    echo -n $ram,$pmem, >> input_perc_access_DRAM_and_PMEM.csv
  
    ram=$(grep Ram ${APP_DATASET[$j]}/autonuma_50/summary_load_access_${APP_DATASET[$j]}.csv | awk -F, '{print $2}')
    pmem=$(grep PMEM ${APP_DATASET[$j]}/autonuma_50/summary_load_access_${APP_DATASET[$j]}.csv | awk -F, '{print $2}')
    echo -n $ram,$pmem, >> input_perc_access_DRAM_and_PMEM.csv
  
    ram=$(grep Ram ${APP_DATASET[$j]}/autonuma_70/summary_load_access_${APP_DATASET[$j]}.csv | awk -F, '{print $2}')
    pmem=$(grep PMEM ${APP_DATASET[$j]}/autonuma_70/summary_load_access_${APP_DATASET[$j]}.csv | awk -F, '{print $2}')
    echo $ram,$pmem >> input_perc_access_DRAM_and_PMEM.csv

    echo ${APP_DATASET[$j]} >> app_dataset.csv
  
done

paste app_dataset.csv  input_perc_access_DRAM_and_PMEM.csv -d , > temp
mv temp input_perc_access_DRAM_and_PMEM.csv 
sed -i '1 i\app_name,dram_30,pmem_30,dram_50,pmem_50,dram_70,pmem_70' input_perc_access_DRAM_and_PMEM.csv 
rm app_dataset.csv
