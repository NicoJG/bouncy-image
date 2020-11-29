import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time

# import other files of this project
from ball import Ball
from boundary import Boundary

# general constants
animation_time = 2 # how many seconds should the animation run
fps = 60 # frames per second
n = 5 # number of balls
boundary = Boundary(-1,1,-1,1) # ball container

# init plot
fig,ax = plt.subplots()
ln = plt.plot([],[],"o")[0]

# init_func called before the first frame
def init_animation():
    global ln,balls
    # init balls
    balls = []
    for i in range(n):
        balls.append(Ball(0,0,"blue"))

    # init limits
    ax.set_xlim(boundary.l, boundary.r)
    ax.set_ylim(boundary.b, boundary.t)
    
    return ln,

# generator function for each frames delta time
def calc_dt():
    starting_time = time.time()
    last_time = starting_time-1/fps
    while last_time-starting_time < animation_time:
        dt = time.time()-last_time # in seconds
        last_time = time.time()
        yield dt

# does the animation
def update_animation(dt):
    global ln,balls
    x_data = []
    y_data = []
    for ball in balls:
        ball.update(dt, boundary)
        x_data.append(ball.x)
        y_data.append(ball.y)
    
    ln.set_data(x_data, y_data)
    return ln,

ani = anim.FuncAnimation(fig, update_animation, frames=calc_dt, init_func=init_animation, interval=1000/fps, blit=True)

plt.show()