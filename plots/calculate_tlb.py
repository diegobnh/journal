import pandas as pd
import glob

dram_file = glob.glob('memory_trace_mapped_dram_*.csv')
pmem_file = glob.glob('memory_trace_mapped_pmem_*.csv')

df_dram = pd.read_csv(dram_file[0])
df_dram_tlb = df_dram.tlb.value_counts(normalize=True).mul(100).round(2).rename_axis('TLB').reset_index(name='Access')
df_dram_tlb.to_csv("dram_tlb_ration.csv", index=False)

df_pmem = pd.read_csv(pmem_file[0])
df_pmem_tlb = df_pmem.tlb.value_counts(normalize=True).mul(100).round(2).rename_axis('TLB').reset_index(name='Access')
df_pmem_tlb.to_csv("pmem_tlb_ration.csv", index=False)
