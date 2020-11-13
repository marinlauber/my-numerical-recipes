import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

t = 0
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
im = ax.imshow(np.random.rand(100, 100), norm=None, cmap="RdBu")
cax = make_axes_locatable(ax).append_axes("right", size="5%", pad="2%")
cb = fig.colorbar(im, cax=cax)
ax.set_xticks([]); ax.set_yticks([])
while(t<=1e2):
    #  update using RK
    im.set_data(np.random.rand(100, 100))
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(1e-9)
    t+=1

