#!/bin/bash
: '
source APP_DATASET.sh

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

        python3 -W ignore ../../calculate_tlb.py

        cd ../..
	done
done
'

grep TLB_miss */autonuma_70/pmem_tlb_ratio.csv | awk -F, '{print $N1}'  | awk -F/ '{print $1}' > app_dataset

grep TLB_miss */autonuma_30/pmem_tlb_ratio.csv | awk -F, '{print $NF}' > tlb_30_pmem
grep TLB_miss */autonuma_50/pmem_tlb_ratio.csv | awk -F, '{print $NF}' > tlb_50_pmem
grep TLB_miss */autonuma_70/pmem_tlb_ratio.csv | awk -F, '{print $NF}' > tlb_70_pmem

grep TLB_miss */autonuma_30/dram_tlb_ratio.csv | awk -F, '{print $NF}' > tlb_30_dram
grep TLB_miss */autonuma_50/dram_tlb_ratio.csv | awk -F, '{print $NF}' > tlb_50_dram
grep TLB_miss */autonuma_70/dram_tlb_ratio.csv | awk -F, '{print $NF}' > tlb_70_dram

paste app_dataset tlb_30_dram tlb_50_dram tlb_70_dram tlb_30_pmem tlb_50_pmem tlb_70_pmem -d, > tlb_ratio.csv

rm -f app_dataset tlb_30_* tlb_50_* tlb_70_*

python3 plot_tlb_ratio.py
