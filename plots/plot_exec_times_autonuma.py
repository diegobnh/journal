import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df.set_index("app_name", inplace=True)
df.plot(kind="bar")

plt.xticks(rotation = 45)
plt.xlabel("Workloads")
plt.ylabel("Execution Time (Min)")

filename = "exec_time_autonuma_mem_pressure.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()
