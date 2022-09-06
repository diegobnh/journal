#!/bin/bash

source app_dataset.sh


rm -f exec_time_*.csv
for ((i = 0; i < ${#TYPES_OF_MEM_PRESSURE[@]}; i++)); do
    for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
  	#-------------------------------------------------------------------------------------------------------------------
  	start=$(sed -n 2p ${APP_DATASET[$j]}/autonuma_${MEM_PRESSURE[$i]}/track_info_${APP_DATASET[$j]}.csv | awk -F, '{print $1}')
	end=$(tail -n 1 ${APP_DATASET[$j]}/autonuma_${MEM_PRESSURE[$i]}/track_info_${APP_DATASET[$j]}.csv | awk -F, '{print $1}')
	exec_time_autonuma=$(echo $start $end | awk '{printf "%.2f", ($2-$1)/60}')

	#start=$(sed -n 2p ${APP_DATASET[$j]}/static_mapping/track_info_${APP_DATASET[$j]}.csv | awk -F, '{print $1}')
	#end=$(tail -n 1 ${APP_DATASET[$j]}/static_mapping/track_info_${APP_DATASET[$j]}.csv | awk -F, '{print $1}')
	#exec_time_static_mapping=$(echo $start $end | awk '{print ($2-$1)/60}')

	#echo -n ${APP_DATASET[$j]},$exec_time_autonuma,$exec_time_static_mapping, >> input_exec_time.csv
	#echo $exec_time_static_mapping $exec_time_autonuma | awk '{print (1-($1/$2))*100}' >> input_exec_time.csv
	#-------------------------------------------------------------------------------------------------------------------
    echo $exec_time_autonuma >> exec_time_${TYPES_OF_MEM_PRESSURE[$i]}.csv
    done
done

rm -f app_dataset.csv
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo ${APP_DATASET[$j]} >> app_dataset.csv
done

paste app_dataset.csv exec_time_30.csv exec_time_50.csv exec_time_70.csv -d , > exec_times.csv
rm -f exec_time_*.csv app_dataset.csv 
