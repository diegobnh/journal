import pandas as pd
import glob

dram_file = glob.glob('memory_trace_mapped_dram_*.csv')
pmem_file = glob.glob('memory_trace_mapped_pmem_*.csv')
store_file = glob.glob('memory_trace_mapped_stores_*.csv')

df_dram = pd.read_csv(dram_file[0])
df_pmem = pd.read_csv(pmem_file[0])
df_store = pd.read_csv(store_file[0])

df_dram_store = pd.merge(df_dram, df_store, on="virt_addr", how="inner").drop_duplicates()
print("dram,",round(len(df_dram_store.virt_addr.unique())/len(df_dram.virt_addr.unique()),4))

df_pmem_store = pd.merge(df_pmem, df_store, on="virt_addr").drop_duplicates()
print("pmem,",round(len(df_pmem_store.virt_addr.unique())/len(df_pmem.virt_addr.unique()),4))
