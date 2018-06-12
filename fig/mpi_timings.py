import matplotlib as mpl
import os
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas
print("imports done")


df = pandas.read_csv('mpi_timings.csv',index_col=0)

df.plot()

print("plot made")
plt.title('Time vs Cores MPI')
plt.savefig('mpi.png')
print("saved")
