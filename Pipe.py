#!/usr/bin/env python
# -*- coding: utf-8 -*-

import keyboard
import numpy as np
import matplotlib.pyplot as plt


class Pipe(object):

    def __init__(self, nx=2001, L=1000, delta=0.4, r=0.73, c=1.0, eps1=0.04, eps2=0.2, ts=0.5):

        # grid size
        self.nx = nx

        # itial conditions u=1, q=0
        self.u = np.ones(self.nx+2)
        self.q = np.zeros(self.nx+2)

        # store params
        self.delta =delta
        self.eps1 = eps1
        self.eps2 = eps2
        self.c_param = c
        self.r_param = r
        dx = L / (nx - 1)
        self.dxi = 1./dx
        self.dxi2 = 1./dx**2

        self.dt = ts*(dx**2/2.)
        self.iter  = 0
        self.piter= 50

    
    def run(self, Niter=50000):

        # plot artist: on
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.ylim(-1,2)
        plt.xlim(1,2001); plt.xticks([])
        line1, = ax.plot(self.u-1.1, label="u")
        line2, = ax.plot(self.q+.1, label="q")
        text = ax.text(50,1.8,'R: '+str(self.r_param),
                       bbox=dict(facecolor='none',edgecolor='k'))
        plt.legend(loc=1)

        while(self.iter<Niter):
            self.update()
            if(self.iter%self.piter==0): # only check every few iteration
                if keyboard.is_pressed('p'):
                    self.puff()
                if keyboard.is_pressed('o'):
                    self.hole()
                if keyboard.is_pressed('up'):
                    self.r_param += 0.005
                if keyboard.is_pressed('down'):
                    self.r_param -= 0.005
                line1.set_ydata(self.u-1.1)
                line2.set_ydata(self.q+.1)
                text.set_text('R: '+str(self.r_param))
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(1e-9)
            self.iter+=1


    def applyBC(self):

        # u BC
        self.u[0] = self.u[self.nx-1]
        self.u[self.nx+1] = self.u[2]
        # q BC
        self.q[0] = self.q[self.nx-1]
        self.q[self.nx+1] = self.q[2]


    def update(self):
        """
        Dwight Barkley (2018), "Simplifying the complexity of pipe flow"
        """

        self.applyBC()
    
        # derivatives
        u_n = -self.c_param*(self.u[1:-1] - self.u[:-2]) * self.dxi
        q_n = (self.q[:-2] - 2.*self.q[1:-1] + self.q[2:]) * self.dxi2

        # other terms
        ukin = self.eps1*(1.-self.u[1:-1]) - self.eps2*self.u[1:-1]*self.q[1:-1] 
        wkin = self.q[1:-1] * (self.u[1:-1] + self.r_param - 1. - (self.r_param + self.delta)*(self.q[1:-1]-1.)**2 )

        # step in place
        self.u[1:-1] += self.dt * (ukin + u_n)
        self.q[1:-1] += self.dt * (wkin + q_n)

        # update exit point
        self.u[0] = self.u[-1]
        self.q[0] = self.q[-1]

        # advect on point, slide grid
        self.u[1:] = self.u[:-1]
        self.q[1:] = self.q[:-1]


    def puff(self):
        # random puff
        start = int(.1*(self.nx-1))
        stop  = int(min(start+20,self.nx))
        self.q[start:stop] += 0.5+0.05*np.random.rand()


    def hole(self):
        # random hole
        start = int(.1*(self.nx-1))
        stop  = int(min(start+20,self.nx))
        self.q[start:stop] = 0.0


if __name__ == "__main__":
    pipe = Pipe()
    pipe.run()
