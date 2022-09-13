import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("max_pmem.csv", names=["app_name", "No_pressure","Pressure_30", "Pressure_50", "Pressure_70"])

df["Pressure_30"] = round(df["Pressure_30"]/df["No_pressure"], 2)
df["Pressure_50"] = round(df["Pressure_50"]/df["No_pressure"], 2)
df["Pressure_70"] = round(df["Pressure_70"]/df["No_pressure"], 2)

df.drop("No_pressure", axis=1, inplace=True)
df.set_index("app_name", inplace=True)
df.plot(kind="bar", figsize=(7, 3))

plt.xticks(rotation = 60)
plt.xlabel("Workloads")
plt.ylabel("Max Allocation in PMEM \n normalized by No pressure")
plt.axhline(1, color='black', linestyle='--')
filename = "max_allocation_in_pmem.pdf"
plt.savefig(filename, bbox_inches="tight")
plt.clf()
