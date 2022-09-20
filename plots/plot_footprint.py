import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np

file = sys.argv[1]

labels = ['10%', '20%', '30%', '40%','50%', '60%', '70%', '80%','90%','100%'] 


df = pd.read_csv(file, names=["footprint","app_name"])
df['footprint'] = round(df['footprint']/1000 , 2)

'''
This code is responsible to convert one column to multiple columns
'''
list_of_applications = list(df.app_name.unique())

#As we have a lot application and to avoid repeat colors we do it.
NUM_COLORS = len(df.app_name.unique())
cmap = plt.get_cmap('nipy_spectral')
colors = [cmap(i) for i in np.linspace(0, 1, NUM_COLORS)]

new_df = pd.DataFrame()
for app in list_of_applications:
    df_app = df.loc[df.app_name == app]
    new_df[app] = df_app['footprint'].values

'''
Now we have a new dataframe where each column represent an application
'''
#First plot
#------------------------------------------------------------------------------------------
ax = new_df.plot(marker='o', color=colors)
ax.set_xticks(np.arange(len(labels)))
ax.set_xticklabels(labels)
#new_df.plot(color=colors, ax=ax)

#plt.title('Memory Footprint Profile')
plt.xlabel('Percentage of Execution Time',fontsize=14)
plt.ylabel('Resident Set Size (GB)', fontsize=14)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

name_file="RSS_vs_time.pdf"
plt.savefig(name_file,dpi=300, bbox_inches='tight', format='pdf')
plt.clf()



#Second plot
#------------------------------------------------------------------------------------------
df_max_pss = df.groupby("app_name")["footprint"].max().reset_index(name='max_footprint')
df_max_pss.sort_values(by="max_footprint", inplace=True)
df_max_pss.set_index("app_name", inplace=True)

ax = df_max_pss.plot.bar(color=[colors],legend=False,figsize=(10, 3))
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=8,xytext = (0, 10), textcoords = 'offset points')

ax.spines['top'].set_visible(False)  
plt.xticks(rotation=60,ha='right') 
#plt.title('Memory Footprint Profile')
plt.xlabel('Applications', fontsize=14)
plt.ylabel('Resident Set Size (MB)', fontsize=14)

name_file="Max_RSS_per_application.pdf"
plt.savefig(name_file,dpi=300, bbox_inches='tight', format='pdf')
plt.clf()


