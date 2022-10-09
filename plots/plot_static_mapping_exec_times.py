import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

df_autonuma = pd.read_csv("../exec_times.csv", names=["app_name", "No_pressure", "Pressure_30", "Pressure_50", "Pressure_70"])
df_autonuma.sort_values(by="app_name", inplace=True)

df_static_1 = pd.read_csv("../static_results_iter1/exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df_static_1.sort_values(by="app_name", inplace=True)

df_static_2 = pd.read_csv("../static_results_iter2/exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df_static_2.sort_values(by="app_name", inplace=True)

df_static_3 = pd.read_csv("../static_results_iter3/exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df_static_3.sort_values(by="app_name", inplace=True)

df = (pd.concat([df_static_1, df_static_2, df_static_3]).reset_index().groupby("index").mean())
df["app_name"] = df_autonuma["app_name"]
df.sort_values(by="app_name", inplace=True)

df_autonuma.set_index("app_name", inplace=True)
df.set_index("app_name", inplace=True)

df["Pressure_30"] = (1 - df["Pressure_30"]/df_autonuma["Pressure_30"]) * 100
df["Pressure_50"] = (1 - df["Pressure_50"]/df_autonuma["Pressure_50"]) * 100
df["Pressure_70"] = (1 - df["Pressure_70"]/df_autonuma["Pressure_70"]) * 100

df.round(decimals = 2).to_csv("static_mapping_gain.csv")
df.mean().round(decimals = 2).to_csv("static_mapping_gain_mean_by_pressure.csv")
#df['app_mean'] = df.mean(axis=1)
#df[['app_mean']].round(decimals = 2).to_csv("static_mapping_gain_mean_by_application.csv")


fig, axs = plt.subplots(3, 1, figsize=(14, 8), sharex=True)
colors = tuple(np.where(df["Pressure_30"]>0, 'tab:blue', 'tab:orange'))
df[["Pressure_30"]].plot(kind="bar", figsize=(7, 3), color=[colors], ax=axs[0])
colors = tuple(np.where(df["Pressure_50"]>0, 'tab:blue', 'tab:orange'))
df[["Pressure_50"]].plot(kind="bar", figsize=(7, 3), color=[colors], ax=axs[1])
colors = tuple(np.where(df["Pressure_70"]>0, 'tab:blue', 'tab:orange'))
df[["Pressure_70"]].plot(kind="bar", figsize=(7, 3), color=[colors], ax=axs[2])

legends=["Pressure 30", "Pressure 50", "Preeesure 70"]
for i in [0,1,2]:
    axs[i].spines['top'].set_visible(False)
    for p in axs[i].patches:
        axs[i].annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')
    axs[i].legend([legends[i]], ncol=1, loc=9,bbox_to_anchor =(0.5, 1.2))
    vals = axs[i].get_yticks()
    axs[i].set_yticklabels(['{:.0f}%'.format(x) for x in vals], fontsize=14)
    axs[i].axhline(0, color='black', linestyle='--')

plt.xticks(fontsize=14, rotation=60)
plt.subplots_adjust(wspace=4, hspace=1)
axs[2].set(xlabel=None)
plt.gcf().set_size_inches(12, 6)
fig.text(0.5, -0.1, 'Workloads', ha='center', fontsize=14)
fig.text(0.05, 0.5, 'Reduction in Execution Time (%)', va='center', rotation='vertical', fontsize=14)

filename = "exec_time_static_mapping_subplot.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()

'''
Plot 1
'''
colors = tuple(np.where(df["Pressure_30"]>0, 'tab:blue', 'tab:orange'))

ax0 = df[["Pressure_30"]].plot(kind="bar", figsize=(7, 3), color=[colors])
ax0.spines['top'].set_visible(False)
ax0.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0, symbol='%', is_latex=False))
for p in ax0.patches:
      ax0.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Reduction in Execution Time (%)")
plt.axhline(0, color='black', linestyle='--')
filename = "exec_time_static_mapping_pressure30.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()

'''
Plot 2 
'''

colors = tuple(np.where(df["Pressure_50"]>0, 'tab:blue', 'tab:orange'))

ax1 = df[["Pressure_50"]].plot(kind="bar", figsize=(7, 3), color=[colors])
ax1.spines['top'].set_visible(False)
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0, symbol='%', is_latex=False))
for p in ax1.patches:
      ax1.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Reduction in Execution Time (%)")
plt.axhline(0, color='black', linestyle='--')
filename = "exec_time_static_mapping_pressure50.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()

'''
Plot 3
'''

colors = tuple(np.where(df["Pressure_70"]>0, 'tab:blue', 'tab:orange'))

ax2 = df[["Pressure_70"]].plot(kind="bar", figsize=(7, 3), color=[colors])
ax2.spines['top'].set_visible(False)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0, symbol='%', is_latex=False))
for p in ax2.patches:
      ax2.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Reduction in Execution Time (%)")
plt.axhline(0, color='black', linestyle='--')
filename = "exec_time_static_mapping_pressure70.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()





'''
Plot 4
'''

#colors = tuple(np.where(df[["Pressure_30", "Pressure_50", "Pressure_70"]]>0, 'tab:blue', 'tab:orange'))

ax2 = df[["Pressure_30", "Pressure_50","Pressure_70"]].plot(kind="bar", figsize=(7, 3)) #, color=[colors])
ax2.spines['top'].set_visible(False)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100, decimals=0, symbol='%', is_latex=False))
#for p in ax2.patches:
#      ax2.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=10,xytext = (0, 14), textcoords = 'offset points')

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Reduction in Execution Time (%)")
plt.axhline(0, color='black', linestyle='--')
filename = "exec_time_static_mapping_all_pressure.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()
