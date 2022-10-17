import pandas as pd
import matplotlib.pyplot as plt

df_external_access = pd.read_csv("../input_perc_access_DRAM_and_PMEM.csv")
df_external_access = df_external_access[df_external_access.columns.drop(list(df_external_access.filter(regex='dram_')))]
df_external_access.sort_values(by="app_name", inplace=True)

df_1 = df_external_access[["app_name","pmem_30"]]
df_1.rename(columns={'pmem_30':'pmem_access'}, inplace=True)
df_2 = df_external_access[["app_name","pmem_50"]]
df_2.rename(columns={'pmem_50':'pmem_access'}, inplace=True)
df_3 = df_external_access[["app_name","pmem_70"]]
df_3.rename(columns={'pmem_70':'pmem_access'}, inplace=True)

df_temp = df_1.append(df_2, ignore_index=True)
df_external_access = df_temp.append(df_3, ignore_index=True)

df_slowdown = pd.read_csv("../exec_times.csv", names=["app_name", "No_pressure", "Pressure_30", "Pressure_50", "Pressure_70"])
df_slowdown.sort_values(by="app_name", inplace=True)
df_slowdown["Pressure_30"] = round(df_slowdown["Pressure_30"]/df_slowdown["No_pressure"], 2)
df_slowdown["Pressure_50"] = round(df_slowdown["Pressure_50"]/df_slowdown["No_pressure"], 2)
df_slowdown["Pressure_70"] = round(df_slowdown["Pressure_70"]/df_slowdown["No_pressure"], 2)
df_slowdown.drop("No_pressure", axis=1, inplace=True)

df_1 = df_slowdown[["app_name","Pressure_30"]]
df_1.rename(columns={'Pressure_30':'slowdown'}, inplace=True)
df_2 = df_slowdown[["app_name","Pressure_50"]]
df_2.rename(columns={'Pressure_50':'slowdown'}, inplace=True)
df_3 = df_slowdown[["app_name","Pressure_70"]]
df_3.rename(columns={'Pressure_70':'slowdown'}, inplace=True)

df_temp = df_1.append(df_2, ignore_index=True)
df_slowdown = df_temp.append(df_3, ignore_index=True)

df_merge = pd.concat([df_external_access,df_slowdown], axis=1)
print(df_merge.sort_values(by="slowdown"))

fig = plt.gcf()
fig.set_size_inches(12, 6)
plt.scatter(df_external_access['pmem_access'], df_slowdown['slowdown'], s=5)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
#bc_urand points
plt.plot(30,1.27, 'o', markersize=2, mec='red', mfc='none', mew=60)
plt.annotate('bc_urand', xy=(32, 1.2),xytext=(33, 1.0),arrowprops=dict(arrowstyle='->',lw=0.5, color="red"), fontsize=10)

#bfs_urand
#plt.plot(1.8,1.73, 'o', markersize=1, mec='red', mfc='none', mew=8)
#plt.annotate('bfs_urand', xy=(2.8, 1.8),xytext=(2.5, 2.0),arrowprops=dict(arrowstyle='->',lw=0.5, color="red"), fontsize=6)

plt.plot(25,2.6, 'o', markersize=2, mec='red', mfc='none', mew=65)
plt.annotate('bc_kron', xy=(28, 2.6),xytext=(29, 2.4),arrowprops=dict(arrowstyle='->',lw=0.5, color="red"), fontsize=10)

plt.xlabel("NVM access (%)", fontsize=14)
plt.ylabel("Slowdown (%)", fontsize=14)
filename = "slowdown_vs_nvm_access.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()

#df_list = []
#df = pd.merge(df_external_access, df_slowdown, how="inner", on=["app_name"])

#df2 = df['Pressure_30'].append(df['Pressure_50']).reset_index(drop=True)
#print(df)
