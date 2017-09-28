import numpy as np
import matplotlib.pyplot as plt
import math

x=np.linspace(-100,100,1000)
y=[]
for i in x:
    y.append(1.0/(1+math.exp(-i)))
plt.plot(x,y)
plt.show()