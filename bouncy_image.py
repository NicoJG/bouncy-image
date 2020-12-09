import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
from PIL import Image

# import other files of this project
from constants import *
from ball import Ball
from boundary import Boundary

# TODO: collisions are kinda weird when multiple collisions happen to one ball on one frame

# init plot
fig,ax = plt.subplots()

# init_func called before the first frame
def init_animation():
    global balls, boundary, scat
    # init balls
    balls = []
    # get image pixels
    img = Image.open(image_path)
    pix = img.load()
    # set boundaries
    boundary = Boundary(-1,img.size[0],-1,img.size[1])
    # set figure size
    fig.set_figwidth(fig_width)
    aspect_ratio = img.width/img.height
    fig.set_figheight(fig_width/aspect_ratio)
    # set axes limits
    ax.set_xlim(boundary.l, boundary.r)
    ax.set_ylim(boundary.b, boundary.t)
    # init balls
    for col in range(img.size[0]):
        for row in range(img.size[1]):
            # TODO: don't use white/grey/transparent pixels
            if pix[col,row][3] > 0:
                x = float(col)
                y = float(img.size[1] - row - 1)
                color = [rgba/255 for rgba in pix[col,row]]
                ball = Ball(x,y,color)
                balls.append(ball)
    # init plot data
    x_data = []
    y_data = []
    color_data = []
    for ball in balls:
        x_data.append(ball.x[0])
        y_data.append(ball.x[1])
        color_data.append(ball.color)

    # calc ball size in points^2 via matplotlib transformations
    r_ = ax.transData.transform([r,0])[0] - ax.transData.transform([0,0])[0] # points
    marker_size = (2*r_)**2 * marker_size_correction_factor # points^2
    # init plot
    scat = ax.scatter(x_data, y_data, c=color_data, s=marker_size)

    return scat,

# generator function for each frames delta time
def calc_dt():
    starting_time = time.time()
    current_time = starting_time-1/fps
    while True:
        last_time = current_time
        current_time = time.time()
        if current_time - starting_time <= animation_start_delay:
            dt = 0.
        elif current_time - starting_time <= animation_start_delay + animation_time:
            if fixed_dt:
                dt = 1/fps
            else:
                dt = current_time-last_time # in seconds
        elif current_time - starting_time <= animation_start_delay + animation_time + animation_end_delay:
            dt = 0.
        else:
            break
        yield dt

# does the animation
def update_animation(dt):
    global balls, scat

    if show_debug_time: print("dt =",dt)
    debug_time("matplotlib",show_debug_time)
    
    # move every ball and check the boundary collision
    for ball in balls:
        ball.move(dt)
        ball.boundary_collision(boundary)
    
    debug_time("move+boundary",show_debug_time)

    balls_by_sector = Ball.sort_balls_in_sectors(balls, boundary)
    
    debug_time("sector_sort",show_debug_time)

    # check every ball pair in every sector
    for key in balls_by_sector:
        balls_in_sector = balls_by_sector[key]
        for i in range(len(balls_in_sector)-1):
            for j in range(i+1,len(balls_in_sector)):
                Ball.ball_collision(balls_in_sector[i],balls_in_sector[j])
    
    debug_time("sector_collisions",show_debug_time)
    
    # update the visuals
    x_data = []
    y_data = []
    for ball in balls:
        x_data.append(ball.x[0])
        y_data.append(ball.x[1])
    scat.set_offsets(np.column_stack((x_data,y_data)))
    
    debug_time("visuals",show_debug_time)

    return scat,

def debug_time(label="elapsed-time",show_msg=True):
    global debug_time_last
    if "debug_time_last" not in globals():
        debug_time_last = 0
    if debug_time_last > 0 and show_msg:
        print(label," = ",time.time()-debug_time_last)
    debug_time_last = time.time()

# animate
ani = anim.FuncAnimation(fig, update_animation, frames=calc_dt, init_func=init_animation, interval=1000/fps, blit=True)

plt.show()