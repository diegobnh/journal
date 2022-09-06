import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np



df = pd.read_csv("mem_footprint.csv", names=["app_name", "rss"])
df['rss'] = round(df['rss']/1000, 2)
list_of_applications = list(df.app_name.unique())


NUM_COLORS = len(df.app_name.unique())
cmap = plt.get_cmap('nipy_spectral')
colors = [cmap(i) for i in np.linspace(0, 1, NUM_COLORS)]

df.set_index("app_name", inplace=True)
df.sort_values("rss", inplace=True)
ax = df.plot.bar(color=[colors],legend=False,figsize=(10, 3))
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.1f'), (p.get_x() + p.get_width() / 2., p.get_height()), rotation=90,ha = 'center', va = 'center',size=6,xytext = (0, 10), textcoords = 'offset points')

ax.spines['top'].set_visible(False)
plt.xticks(rotation=45,ha='right')
plt.title('Memory Footprint Profile')
plt.xlabel('Applications')
plt.ylabel('Resident Set Size (GB)')

name_file="RSS_per_application_sorted.pdf"
plt.savefig(name_file,dpi=300, bbox_inches='tight', format='pdf')
plt.clf()
