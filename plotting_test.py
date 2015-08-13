__author__ = 'hetianyi'

import matplotlib.pyplot as plt
import matplotlib.animation as animate
import random as rng
import numpy as np
import scipy.io.wavfile as siow


# Set up Parameters & Init.

# Streaming Audio Data read
# filename = '80s.wav'
# (Fs,input) = siow.read(filename)


fig = plt.figure()
ax1 = fig.add_subplot(111)
maxelem = 20    # Max Data Collected


x = []
y = []

# Define function to be called
def plottest(i):
    # print(i)
    # Restrict the max length
    if len(x) >= maxelem:
        x.pop(0)
        y.pop(0)

    # Adding new data
    x.append(i)
    y.append(rng.randint(0,20)) # Streaming Random Data from 0 - 20
    # y.append(input[i])  # Streaming Audio data

    ax1.clear()
    ax1.plot(x,y)

    # Some Other Feature I wish to Have:
    # 1. Y-Axis Fixed for the graph

# Animation, Maybe there exists a better way?
ani = animate.FuncAnimation(fig,plottest,interval=500)
plt.show()
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()

x = np.arange(0, 2*np.pi, 0.01)        # x-array
line, = ax.plot(x, np.sin(x))

def animate(i):
    line.set_ydata(np.sin(x+i/10.0))  # update the data
    return line,

#Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,

ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
    interval=25)
plt.show()
"""