import glob
import pandas as pd
import sys


CHUNK_SIZE=500000000
file = glob.glob('track_info_*.csv')
name = file[0].split('.')[0]
app_dataset = name.split('_')[-2] + "_" + name.split('_')[-1]

mmap_file_name="mmap_trace_" + app_dataset + ".csv"
df = pd.read_csv(mmap_file_name, names=['ts_event_start','mmap','size_allocation', 'start_addr_hex','call_stack_hash', 'call_stack_hexadecimal'])
df["chunk_flag"] = ""
df["chunk_id"] = ""
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
           new_row=[row['ts_event_start'], row['mmap'], CHUNK_SIZE, new_start_addr, row['call_stack_hash'], row['call_stack_hexadecimal'], row['start_addr_decimal'], 1, i]
           print(new_row)
           df.loc[df.shape[0]] = new_row
           i = i + 1;
        if(remnant_size > 0):
           new_start_addr = hex(row['start_addr_decimal'] + (i * CHUNK_SIZE))
           new_row=[row['ts_event_start'], row['mmap'], remnant_size, new_start_addr, row['call_stack_hash'], row['call_stack_hexadecimal'], row['start_addr_decimal'], 1, i]
           print(new_row)
           df.loc[df.shape[0]] = new_row
        index_list_to_drop.append(index)
     else:
        new_row=[row['ts_event_start'], row['mmap'], row['size_allocation'], row['start_addr_hex'], row['call_stack_hash'], row['call_stack_hexadecimal'], row['start_addr_decimal'], 0, 0]
        print(new_row)
        df.loc[df.shape[0]] = new_row
        index_list_to_drop.append(index)
        #df.at[index,'chunk_flag'] = 0
        #df.at[index,'chunk_id'] = 0
        

df = df.drop(index=index_list_to_drop)
#df.drop('start_addr_decimal', axis=1, inplace=True)
df.sort_values(by=['ts_event_start', 'start_addr_hex'], ascending=True, inplace=True)


output_filename="mmap_trace_by_chunk_" + app_dataset + "_v2.csv"
df.to_csv(output_filename, index=False)
