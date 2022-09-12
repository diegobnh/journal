import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../exec_times.csv", names=["app_name", "No_pressure", "Pressure_30", "Pressure_50", "Pressure_70"])
df = df[["app_name", "No_pressure"]]

df.set_index("app_name", inplace=True)
df.sort_values(by="No_pressure", inplace=True)

ax = df.plot(kind="bar", figsize=(7, 3), legend=False)
ax.spines['top'].set_visible(False)

for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=6,xytext = (0, 10), textcoords = 'offset points')

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Execution Time (min)")
filename = "exec_time_autonuma_not_pressure.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()
