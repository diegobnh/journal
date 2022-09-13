#!/bin/bash

source app_dataset.sh

rm -f mem_footprint.csv memory_pressure*.csv

echo -n "MEM_PRESSURE_30=(" >> memory_pressure_30.csv
echo -n "MEM_PRESSURE_50=(" >> memory_pressure_50.csv
echo -n "MEM_PRESSURE_70=(" >> memory_pressure_70.csv

for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    #-------------------------------------------------------------------------------------------------------------------
    mem_footprint=$(cat ${APP_DATASET[$j]}/autonuma/track_info_${APP_DATASET[$j]}.csv | awk -F, 'NR>1{print $2+$3}' | datamash max 1)
    #echo -n $mem_footprint

    pressure=`echo "(($mem_footprint) *  (70/100))" | bc -l`
    pressure=`echo "((18000 - $pressure))" `
    gb_pressure=`echo "(($pressure/1000))" | bc`
    echo -n "\"$gb_pressure\" " >> memory_pressure_30.csv

    pressure=`echo "(($mem_footprint) *  (50/100))" | bc -l`
    pressure=`echo "((18000 - $pressure))" `
    gb_pressure=`echo "(($pressure/1000))" | bc`
    echo -n "\"$gb_pressure\" " >> memory_pressure_50.csv

    pressure=`echo "(($mem_footprint) *  (30/100))" | bc -l`
    pressure=`echo "((18000 - $pressure))" `
    gb_pressure=`echo "(($pressure/1000))" | bc`
    echo -n "\"$gb_pressure\" " >> memory_pressure_70.csv

    echo ${APP_DATASET[$j]},$mem_footprint >> mem_footprint.csv
    #-------------------------------------------------------------------------------------------------------------------
done

echo  ")" >> memory_pressure_30.csv
echo  ")" >> memory_pressure_50.csv
echo  ")" >> memory_pressure_70.csv

cat memory_pressure_* > memory_pressure.csv
cat app_dataset.sh.bkp memory_pressure.csv > app_dataset.sh
rm memory_pressure*.csv
