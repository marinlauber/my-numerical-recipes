import keyboard
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

        x = np.linspace(-1,1,256)
        y = np.zeros_like(x)

        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.ylim(0, 1)
        line, = ax.plot(x, y, '-k')
        
        while True:
            if keyboard.is_pressed('x'):
                print('You pressed x')
                break
            if keyboard.is_pressed('p'):
                print('puff!')
                start = np.random.randint(0,240)
                stop = start+np.random.randint(0,10)
                y[start:stop] += 0.1
            line.set_ydata(y)
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(1e-9)
  