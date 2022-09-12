import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
import math
import os

#read the te input file
input_file = sys.argv[1]
df = pd.read_csv(input_file)

#get app_name from input file
app_dataset = input_file.rsplit('.', 1)[0] #remove the extension
dataset = app_dataset.rsplit('_')[-1]
app = app_dataset.rsplit('_')[-2]
app_dataset = app + "_" + dataset
output_file = app_dataset + "_footprint.csv"


#split the traces in 10 pieces and calculate metrics for each one
number_of_chunks = 10
footprint_avg_per_slot = []
nrows = df.shape[0]
chunk_size = int(nrows/number_of_chunks)

#calculate the average for each chunk
indices = list(range(chunk_size, math.ceil(nrows / chunk_size) * chunk_size, chunk_size))
chunks = np.split(df, indices)
count=0
for small_df in chunks:
	if(count>9):
	  break

	footprint_avg = small_df['dram_app'].mean() + small_df['pmem_app'].mean()
	footprint_avg_per_slot.append(round(footprint_avg,2))
	count+=1


df = pd.DataFrame(footprint_avg_per_slot, columns = ["footprint"])
df['app_name'] = app_dataset
df.to_csv(output_file,index=False, header=None)
