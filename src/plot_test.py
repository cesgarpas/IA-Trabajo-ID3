import matplotlib
import matplotlib.pyplot as plt
import numpy as np

print(len(range(0,100,1)))
# Data for plotting
t = np.arange(0, 5, 1)
s = [1,2,3,4,75]

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='quorum (int)', ylabel='hit rate (%/100)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()