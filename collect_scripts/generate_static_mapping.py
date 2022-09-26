from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import glob
import sys
import math
import os

'''
for ((j = 0; j < ${#APP_DATASET[@]}; j++)); do
    echo "Running:"${APP_DATASET[$j]}

    cd ${APP_DATASET[$j]}/autonuma
    python3 ../../generate_static_mapping.py
    cd ../..
done

'''

def generate_abs_llcm_per_object(app_dataset, df_DRAM, df_PMEM):
    df = df_DRAM.append(df_PMEM, ignore_index = True)
    df_normalized = df['call_stack_hash'].value_counts(normalize=True).mul(100).round(2).rename_axis('call_stack_hash').reset_index(name='perc_access')
    filename = "absolute_llcm_per_obj_"+ app_dataset + ".csv"
    df_normalized.to_csv(filename, index=False)

    dram_normalized = df_DRAM['call_stack_hash'].value_counts(normalize=True).mul(100).round(2).rename_axis('call_stack_hash').reset_index(name='perc_access')
    dram_real = df_DRAM['call_stack_hash'].value_counts(normalize=False).rename_axis('call_stack_hash').reset_index(name='num_access')
    dram = pd.merge(dram_normalized, dram_real, how="inner", on=["call_stack_hash"])
    filename = "absolute_llcm_per_obj_in_DRAM_"+ app_dataset + ".csv"
    dram.to_csv(filename, index=False)
    
    pmem_normalized = df_PMEM['call_stack_hash'].value_counts(normalize=True).mul(100).round(2).rename_axis('call_stack_hash').reset_index(name='perc_access')
    pmem_real = df_PMEM['call_stack_hash'].value_counts(normalize=False).rename_axis('call_stack_hash').reset_index(name='num_access')
    pmem = pd.merge(pmem_normalized, pmem_real, how="inner", on=["call_stack_hash"])
    filename = "absolute_llcm_per_obj_in_PMEM_"+ app_dataset + ".csv"
    pmem.to_csv(filename, index=False)
def analysis_outside_from_cache(app_dataset, df_DRAM, df_PMEM):
    original_stdout = sys.stdout
    with open('analysis_samples_outside_from_cache.txt', 'w') as f:
        sys.stdout = f
    
        print("#########")
        print(app_dataset)
        print("#########")
        
        df_DRAM['virt_page_number'] = df_DRAM['virt_addr'].apply(lambda x: int(x, 16) >> 12)
        df_DRAM['physical_page_number'] = df_DRAM['phys_addr'].apply(lambda x: int(x, 16) >> 12)
        
        df_PMEM['virt_page_number'] = df_PMEM['virt_addr'].apply(lambda x: int(x, 16) >> 12)
        df_PMEM['physical_page_number'] = df_PMEM['phys_addr'].apply(lambda x: int(x, 16) >> 12)
        
        print("DRAM_samples:", round(df_DRAM.shape[0]/(df_DRAM.shape[0]  + df_PMEM.shape[0] ) * 100 ,2),"%")
        print("PMEM_samples:", round(df_PMEM.shape[0]/(df_DRAM.shape[0]  + df_PMEM.shape[0] ) * 100 ,2),"%")

        total_external_access_cost = df_DRAM["access_weight"].sum() + df_PMEM["access_weight"].sum()
        dram_access_cost = 100 * (df_DRAM.access_weight.sum()/total_external_access_cost)
        pmem_access_cost = 100 * (df_PMEM.access_weight.sum()/total_external_access_cost)

        print("\nTotal DRAM cost (sum weight latency):", round(dram_access_cost,2),"%")
        print("Total PMEM cost (sum weight latency):", round(pmem_access_cost,2),"%")
        
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        df_dram_tlb_hit = df_DRAM.loc[df_DRAM.tlb == "TLB_hit"]
        df_dram_tlb_miss = df_DRAM.loc[df_DRAM.tlb == "TLB_miss"]
        print("\nDRAM ratio TLB hit:", round((df_dram_tlb_hit.shape[0]/df_DRAM.shape[0])*100,2),"%")
        print("DRAM ratio TLB miss:", round((df_dram_tlb_miss.shape[0]/df_DRAM.shape[0])*100,2),"%")
        print("\nDRAM TLB hit mean cost:",round(df_dram_tlb_hit.access_weight.mean(),2))
        print("DRAM TLB miss mean cost:",round(df_dram_tlb_miss.access_weight.mean(),2))
        
        df_pmem_tlb_hit = df_PMEM.loc[df_PMEM.tlb == "TLB_hit"]
        df_pmem_tlb_miss = df_PMEM.loc[df_PMEM.tlb == "TLB_miss"]
        print("\nPMEM ratio TLB hit:", round((df_pmem_tlb_hit.shape[0]/df_PMEM.shape[0])*100,2),"%")
        print("PMEM ratio TLB miss:", round((df_pmem_tlb_miss.shape[0]/df_PMEM.shape[0])*100,2),"%")
        print("\nPMEM TLB hit mean cost:",round(df_pmem_tlb_hit.access_weight.mean(),2))
        print("PMEM TLB miss mean cost:",round(df_pmem_tlb_miss.access_weight.mean(),2))
        
        page_number_types = ["virt_page_number", "physical_page_number"]
        for page_number in page_number_types:
            print("\nType of page number:", page_number)
            
            #count how many access per page
            df_DRAM_and_PMEM = pd.concat([df_DRAM, df_PMEM], ignore_index=True)
            df_access_per_page = df_DRAM_and_PMEM[page_number].value_counts().reset_index()
            df_access_per_page.columns = [page_number, 'total_access']

            #filter pages with access at least two access
            df_at_least_two_access = df_access_per_page.loc[df_access_per_page.total_access > 1]
            print("Ratio (DRAM and PMEM):", round((df_at_least_two_access.shape[0]/df_access_per_page.shape[0])*100,2), "% outside from cache with more than one touch")
            
            df_access_per_page = df_DRAM[page_number].value_counts().reset_index()
            df_access_per_page.columns = [page_number, 'total_access']
            df_at_least_two_access = df_access_per_page.loc[df_access_per_page.total_access > 1]
            print("Ratio (DRAM):", round((df_at_least_two_access.shape[0]/df_access_per_page.shape[0])*100,2), "% outside from cache with more than one touch")

            df_access_per_page = df_PMEM[page_number].value_counts().reset_index()
            df_access_per_page.columns = [page_number, 'total_access']
            df_at_least_two_access = df_access_per_page.loc[df_access_per_page.total_access > 1]
            print("Ratio (PMEM):", round((df_at_least_two_access.shape[0]/df_access_per_page.shape[0])*100,2), "% outside from cache with more than one touch")

        print("-------------------------------------------------------------------------------------")
        sys.stdout = original_stdout
def decide_static_mapping_between_DRAM_and_PMEM(app_dataset, df_DRAM, df_PMEM):
    original_stdout = sys.stdout # Save a reference to the original standard output
    #result = subprocess.run(['pwd'], stdout=subprocess.PIPE)

    df_footprint = pd.read_csv("../../mem_footprint.csv", names=["app_name", "mem_footprint"])
    mem_footprint = df_footprint.loc[df_footprint["app_name"] == app_dataset, 'mem_footprint'].iloc[0]
    if mem_footprint > 18000:
      mem_footprint = 18000

    pressures_list=[30, 50, 70]
    for pressure in pressures_list:
        #factor = int(result.stdout.decode('utf-8').strip().split('_')[-1])
        mem_to_remove = int(mem_footprint * ((100-pressure)/100))
        mem_to_remove = int((18000 - mem_to_remove)/1000)
        mem_available = 18 - mem_to_remove
        #print("App:", app_dataset, " Memfootprint:", mem_footprint, " Removed(GB):", pressure,  " Mem Available(GB):", mem_available)

        output_file="static_mapping_" + str(pressure) + ".txt"
        with open(output_file, 'w') as f:
            sys.stdout = f

            df = df_DRAM.append(df_PMEM, ignore_index = True)

            df_access = df['call_stack_hash'].value_counts(normalize=True).mul(100).round(2).reset_index()
            df_access.columns = ['call_stack_hash', 'perc_access']

            filename = "mmap_trace_mapped_" + app_dataset + ".csv"
            df_mmap = pd.read_csv(filename)

            df_num_alloc = df_mmap.groupby("call_stack_hash")['size_allocation'].count().to_frame(name="num_alloc").reset_index()

            df_size = df_mmap.groupby("call_stack_hash")['size_allocation'].first().to_frame(name="size").reset_index()
            df_size['size'] = df_size['size']/1e9
            df_size['size'] = df_size['size'].round(2)

            df = pd.merge(df_access, df_size, on="call_stack_hash")
            df = pd.merge(df, df_num_alloc, on="call_stack_hash")

            df['metric'] = df['perc_access']/df['size']
            df["metric"] = df["metric"].round(2)
            df.sort_values(by='metric', ascending=False, inplace=True)

            output_file="sorted_obj_by_metric_" + str(pressure) + ".csv"
            df.to_csv(output_file, index=False)

            dram_list=[]
            pmem_list=[]
            dram_capacity = mem_available

            for index, row in df.iterrows():
                if (dram_capacity - row['size']) > 0:
                    dram_capacity = dram_capacity - row['size']
                    dram_list.append(row['call_stack_hash'])
                else:
                    pmem_list.append(row['call_stack_hash'])
            #print("Objects to DRAM:")
            dram_list = [int(float(x)) for x in dram_list]
            print(len(dram_list))
            for stack_hash in dram_list:
                print(stack_hash)
            #print("Objects to PMEM:")
            #pmem_list = [int(float(x)) for x in pmem_list]
            #print(pmem_list)

            '''
            dram_list=[]
            pmem_list=[]
            for index, row in df.iterrows():
                if (row['size']) < 100:
                    dram_list.append(row['call_stack_hash'])
                else:
                    pmem_list.append(row['call_stack_hash'])
            print("\nShared Library Mapping:")
            print("-------------------------")
            print("Objects to DRAM:")
            print(dram_list)
            print("Objects to PMEM:")
            print(pmem_list)
            '''
            sys.stdout = original_stdout ## Reset the standard output to its original value

def main():
    files_dram = glob.glob('memory_trace_mapped_dram_*.csv')
    files_pmem = glob.glob('memory_trace_mapped_pmem_*.csv')

    application_dataset = []
    for file in files_dram:
        name = file.split('.')[0]
        app = name.split('_')[-2] + "_" + name.split('_')[-1]
        application_dataset.append(app)

    for file_dram,file_pmem,app_dataset in zip(files_dram,files_pmem, application_dataset):
        df_DRAM = pd.read_csv(file_dram)
        df_PMEM = pd.read_csv(file_pmem)

        #generate_abs_llcm_per_object(app_dataset, df_DRAM, df_PMEM)
        decide_static_mapping_between_DRAM_and_PMEM(app_dataset, df_DRAM, df_PMEM)
            

    
if __name__ == "__main__":
   main()
