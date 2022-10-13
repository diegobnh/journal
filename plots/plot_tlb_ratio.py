import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import glob
import sys

headers=["app_name","dram_tlb_miss_30","dram_tlb_miss_50","dram_tlb_miss_70","pmem_tlb_miss_30","pmem_tlb_miss_50","pmem_tlb_miss_70"]
df = pd.read_csv("tlb_ratio.csv", names=headers)
df.sort_values(by="app_name", inplace=True)

fig, axarr = plt.subplots(3, 1, figsize=(12, 6), sharex=True)

df.plot(x="app_name", y=["dram_tlb_miss_30", "pmem_tlb_miss_30"], kind="bar", ax=axarr[0])
df.plot(x="app_name", y=["dram_tlb_miss_50", "pmem_tlb_miss_50"], kind="bar", ax=axarr[1])
df.plot(x="app_name", y=["dram_tlb_miss_70", "pmem_tlb_miss_70"], kind="bar", ax=axarr[2])

axarr[0].spines['top'].set_visible(False)
for p in axarr[0].patches:
    axarr[0].annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), 
rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')
axarr[0].legend(["DRAM TLB miss","NVM TLB miss"], ncol=2, loc='best', bbox_to_anchor =(1, 1.7))
vals = axarr[0].get_yticks()
axarr[0].set_yticklabels(['{:.0f}%'.format(x) for x in vals], fontsize=14)
axarr[0].set_title("Pressure 30", x=0.5, y=1.3)

axarr[1].spines['top'].set_visible(False)
for p in axarr[1].patches:
    axarr[1].annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()),
rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')
#axarr[1].legend(["DRAM TLB miss","PMEM TLB miss"], ncol=2, loc='best', bbox_to_anchor =(1, 1))
axarr[1].get_legend().remove()
vals = axarr[1].get_yticks()
axarr[1].set_yticklabels(['{:.0f}%'.format(x) for x in vals], fontsize=14)
axarr[1].set_title("Pressure 50", x=0.5, y=1.3)

axarr[2].spines['top'].set_visible(False)
for p in axarr[2].patches:
    axarr[2].annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()),
rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 12.9), textcoords = 'offset points')
#axarr[2].legend(["DRAM TLB miss","PMEM TLB miss"], ncol=2, loc='best', bbox_to_anchor =(1, 1))
axarr[2].get_legend().remove()
vals = axarr[2].get_yticks()
axarr[2].set_yticklabels(['{:.0f}%'.format(x) for x in vals], fontsize=14)
axarr[2].set_title("Pressure 70", x=0.5, y=1.1)

plt.xticks(fontsize=14, rotation=60)
plt.subplots_adjust(wspace=5, hspace=0.8)

fig.text(0.5, -0.08, 'Workloads', ha='center', fontsize=14)
fig.text(0.04, 0.5, 'Percentage of TLB miss in DRAM and PMEM', va='center', rotation='vertical', fontsize=14)

axarr[2].set(xlabel=None)
filename = "tlb_ratio.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()

