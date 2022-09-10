import glob
import pandas as pd
import sys


CHUNK_SIZE=500000000
file = glob.glob('track_info_*.csv')
name = file[0].split('.')[0]
app_dataset = name.split('_')[-2] + "_" + name.split('_')[-1]

mmap_file_name="munmap_trace_" + app_dataset + ".csv"
df = pd.read_csv(mmap_file_name, names=['ts_event_start','munmap','start_addr_hex','size_allocation'])

df['ts_event_start'] = pd.to_numeric(df['ts_event_start'])
df['start_addr_decimal'] = df['start_addr_hex'].apply(int, base=16)

index_list_to_drop = []
for index, row in df.iterrows():
     if(row['size_allocation'] > CHUNK_SIZE):
        i=0
        total_obj = int(row['size_allocation']/CHUNK_SIZE)
        remnant_size = row['size_allocation'] - (total_obj * CHUNK_SIZE);
        start_addr = row['start_addr_decimal']

        while(i < total_obj):
           new_start_addr = hex(row['start_addr_decimal'] + (i * CHUNK_SIZE))
           new_row=[row['ts_event_start'], row['munmap'], new_start_addr, CHUNK_SIZE, row['start_addr_decimal']]
           df.loc[df.shape[0]] = new_row
           i = i + 1;
        if(remnant_size > 0):
           new_start_addr = hex(row['start_addr_decimal'] + (i * CHUNK_SIZE))
           new_row=[row['ts_event_start'], row['munmap'], new_start_addr, remnant_size, row['start_addr_decimal']]
           df.loc[df.shape[0]] = new_row
        index_list_to_drop.append(index)

df = df.drop(index=index_list_to_drop)
df.drop('start_addr_decimal', axis=1, inplace=True)
df.sort_values(by=['ts_event_start', 'start_addr_hex'], ascending=True, inplace=True)

output_filename="munmap_trace_by_chunk_" + app_dataset + ".csv"
df.to_csv(output_filename, index=False)
