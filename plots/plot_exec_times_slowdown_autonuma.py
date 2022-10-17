import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../exec_times.csv", names=["app_name", "No_pressure", "Pressure_30", "Pressure_50", "Pressure_70"])
df.sort_values(by="app_name", inplace=True)
df["Pressure_30"] = round(df["Pressure_30"]/df["No_pressure"], 2)
df["Pressure_50"] = round(df["Pressure_50"]/df["No_pressure"], 2)
df["Pressure_70"] = round(df["Pressure_70"]/df["No_pressure"], 2)

df.drop("No_pressure", axis=1, inplace=True)
df.set_index("app_name", inplace=True)
print(df.describe())

ax = df.plot(kind="bar", figsize=(7, 3), width=0.8)

bars = ax.patches
hatches = ''.join(h*len(df) for h in 'x.O')
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)
ax.legend(["Pressure 30","Pressure 50", "Pressure 70"], ncol=1, loc='best') #, bbox_to_anchor =(1, 1))

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Slowdown Normalized by No Pressure")
plt.axhline(1, color='black', linestyle='--')
filename = "exec_time_autonuma_mem_pressure.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()
