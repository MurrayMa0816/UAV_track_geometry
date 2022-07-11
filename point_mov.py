# -*- coding: utf-8 -*-

from cgi import print_arguments
from matplotlib import pyplot as plt
from matplotlib import animation

from matplotlib.pyplot import MultipleLocator
import numpy as np

class Particle:
    def __init__(self, x, y, x_vel,y_vel):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel

class ParticleSimulator:
    def __init__(self, particles):
        self.particles = particles
    global bool
    global bool_x
    bool=True
    bool_x=True
    print("par",)
    def evolve(self, dt):
        global bool,bool_x
        timestep = 0.00001
        nsteps = int(dt / timestep)
        for p in self.particles:
            if p.y>=950:
                bool=False
                break
            elif p.y<=40:
                bool=True

        if bool==True:
            for i in range(nsteps):
                for p in self.particles:
                    # d_x = timestep * p.x_vel
                    d_y = timestep * p.y_vel 
                    # p.x =p.x+d_x
                    p.y =p.y+d_y
        elif bool==False :
            for i in range(nsteps):
                for p in self.particles:
                    # d_x = timestep * p.x_vel
                    d_y = timestep * -p.y_vel 
                    # p.x =p.x+d_x
                    p.y =p.y+d_y
                    if  p.y<=40:
                        bool=True 


        for p in self.particles:
            if p.x>=1560:
                bool_x=False
                break
            elif p.x<=40:
                bool_x=True

        if bool_x==True:
            for i in range(nsteps):
                for p in self.particles:
                    d_x = timestep * p.x_vel
                    # d_y = timestep * p.y_vel 
                    p.x =p.x+d_x
                    # p.y =p.y+d_y
        elif bool_x==False :
            for i in range(nsteps):
                for p in self.particles:
                    d_x = timestep * -p.x_vel
                    # d_y = timestep * -p.y_vel 
                    p.x =p.x+d_x
                    # p.y =p.y+d_y
                    if  p.x<=40:
                        bool_x=True 
     
     

def visualize(simulator):
    X = [p.x for p in simulator.particles]
    Y = [p.y for p in simulator.particles]

    fig = plt.figure()
    ax = plt.subplot(111, aspect = 'equal')

    # x_major_locator=MultipleLocator(10)
    # #把x轴的刻度间隔设置为1，并存在变量里
    # y_major_locator=MultipleLocator(100)
    # #把y轴的刻度间隔设置为10，并存在变量里
    # ax=plt.gca()
    # ax.set_aspect(0.1)
    # #ax为两条坐标轴的实例
    # ax.xaxis.set_major_locator(x_major_locator)
    # #把x轴的主刻度设置为1的倍数
    # ax.yaxis.set_major_locator(y_major_locator)


    line, = ax.plot(X, Y, 'ro')

    plt.xlim(0, 100)
    plt.ylim(0, 1000)

    def init():
        line.set_data([], [])
        return line,
 
    def animate(aa):
        print(aa)
        simulator.evolve(0.01)
        X = [p.x for p in simulator.particles]
        Y = [p.y for p in simulator.particles]

        line.set_data(X, Y)
        return line,

    anim = animation.FuncAnimation(fig,
                                   animate,
                                   frames=10,
                                   init_func = init,
                                   blit = True,
                                   interval = 10)
    plt.show()

    
particles=[]
def particle_produce(n_edge,num_point):
    particles=[]
    particlestemp=[]
    xx = np.random.randint(20,80, n_edge)
    yy = np.random.randint(30,70, n_edge)
    z = np.random.random(size=[xx.size, num_point])
    x = (z / sum(z)).T.dot(xx)
    y = (z / sum(z)).T.dot(yy)
    x_v= np.random.uniform(2,5,size=(num_point))
    y_v= np.random.uniform(28,30,size=(num_point))
    for i in range(num_point):
        particles.append(Particle(x[i],y[i],x_v[i],y_v[i]))
        particlestemp.append([x[i],y[i]])
    print("particle",particlestemp)
    print("xx",x)
    print("yy",y)
    print("x",x)
    print("y",y)
    print("v",x_v)
    return particles,particlestemp

def test_visualize():
    # particles = [Particle(0.3, 0.5, 1),
    #              Particle(0.0, -0.5, -1),
    #              Particle(-0.1, -0.4, 3)]
    particles, _=particle_produce(8,10)
    print(particles)
    print("nb", particles[0])
    simulator = ParticleSimulator(particles)
    print("simulator",simulator)
    visualize(simulator)
if __name__ == '__main__':
    test_visualize()
