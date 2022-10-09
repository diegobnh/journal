import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

df_autonuma = pd.read_csv("exec_times.csv", names=["app_name", "No_pressure", "Pressure_30", "Pressure_50", "Pressure_70"])
df_autonuma.sort_values(by="app_name", inplace=True)

df_static_1 = pd.read_csv("static_results_iter1/exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df_static_1.sort_values(by="app_name", inplace=True)
df1 = pd.DataFrame()
df1["Pressure_30"] = (1 - df_static_1["Pressure_30"]/df_autonuma["Pressure_30"]) * 100
df1["Pressure_50"] = (1 - df_static_1["Pressure_50"]/df_autonuma["Pressure_50"]) * 100
df1["Pressure_70"] = (1 - df_static_1["Pressure_70"]/df_autonuma["Pressure_70"]) * 100

df_static_2 = pd.read_csv("static_results_iter2/exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df_static_2.sort_values(by="app_name", inplace=True)
df2 = pd.DataFrame()
df2["Pressure_30"] = (1 - df_static_2["Pressure_30"]/df_autonuma["Pressure_30"]) * 100
df2["Pressure_50"] = (1 - df_static_2["Pressure_50"]/df_autonuma["Pressure_50"]) * 100
df2["Pressure_70"] = (1 - df_static_2["Pressure_70"]/df_autonuma["Pressure_70"]) * 100

df_static_3 = pd.read_csv("static_results_iter3/exec_times.csv", names=["app_name", "Pressure_30", "Pressure_50", "Pressure_70"])
df_static_3.sort_values(by="app_name", inplace=True)
df3 = pd.DataFrame()
df3["Pressure_30"] = (1 - df_static_3["Pressure_30"]/df_autonuma["Pressure_30"]) * 100
df3["Pressure_50"] = (1 - df_static_3["Pressure_50"]/df_autonuma["Pressure_50"]) * 100
df3["Pressure_70"] = (1 - df_static_3["Pressure_70"]/df_autonuma["Pressure_70"]) * 100

df_mean = (pd.concat([df1, df2, df3]).reset_index().groupby("index").mean())
print(df_mean.round(decimals = 2))

print("\n\nMEAN")
print("------")
print(df_mean.mean().round(decimals = 2))

print("\nMIN")
print("------")
print(df_mean.min().round(decimals = 2))

print("\nMAX")
print("------")
print(df_mean.max().round(decimals = 2))

df_std = (pd.concat([df_static_1, df_static_2, df_static_3]).reset_index().groupby("index").std())
print(df_std.round(decimals = 2))
print(df_std.mean().round(decimals = 2))
