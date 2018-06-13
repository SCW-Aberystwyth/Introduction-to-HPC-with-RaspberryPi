import matplotlib as mpl
import os
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas
print("imports done")


df = pandas.read_csv('pymp_timings.csv',index_col=0)

df.plot(legend=None)

print("plot made")

plt.xlabel('Cores')
ax = df.plot(legend=None)
ax.set_ylim(0,60)
ax.set_xticks(range(1,17,1))
ax.set_yticks(range(0,60,5))
ax.set_ylabel('Time')
ax.set_title('Time vs Cores PyMP')
ax.grid()

plt.savefig('pymp.svg',dpi=200)

print("saved")
