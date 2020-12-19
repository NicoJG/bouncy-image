import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time
from PIL import Image
from image_manipulation import load_image

# import other files of this project
from constants import *
from ball import Ball
from boundary import Boundary

# get image
img, aspect_ratio = load_image()
# set boundaries
boundary = Boundary(-1,img.size[0],-1,img.size[1])
# init figure and axes
fig = plt.figure(figsize=(fig_height*aspect_ratio,fig_height), dpi=video_height/fig_height)
ax = fig.add_axes(rect=[0.,0.,1.,1.])
# hide axis
ax.set_axis_off()
# set axes limits
ax.set_xlim(boundary.l, boundary.r)
ax.set_ylim(boundary.b, boundary.t)

# init_func called before the first frame
def init_animation():
    global balls, scat
    # init balls
    balls = []
    for col in range(img.size[0]):
        for row in range(img.size[1]):
            if img.getpixel((col,row))[3] > 0:
                x = float(col)
                y = float(img.size[1] - row - 1)
                # rgba 0-255 to rgba 0-1
                color = [rgba/255 for rgba in img.getpixel((col,row))]
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

    # calc ball size in points^2
    # 1 point == fig.dpi/72. pixels
    r_ = r * (video_height/boundary.height) * (72/fig.dpi) # points
    marker_size = (2*r_)**2 * marker_size_correction_factor # points^2
    # init plot
    scat = ax.scatter(x_data, y_data, c=color_data, s=marker_size)
    return scat,

# generator function for each frames delta time in seconds
def calc_dt():
    global frame_count
    frame_count = 0
    starting_time = time.time()
    current_time = starting_time-1/fps
    while True:
        last_time = current_time
        if fixed_dt:
            current_time += 1/fps
        else:
            current_time = time.time()
        if current_time - starting_time <= animation_start_delay:
            dt = 0.
        elif current_time - starting_time <= animation_start_delay + animation_time:
            if fixed_dt:
                dt = 1/fps
            else:
                dt = current_time-last_time
        elif current_time - starting_time <= animation_start_delay + animation_time + animation_end_delay:
            dt = 0.
        else:
            break
        frame_count += 1
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

# estimate frame count
frame_count_estimate = fps * (animation_start_delay + animation_time + animation_end_delay)

# animate
ani = anim.FuncAnimation(fig, func=update_animation, frames=calc_dt, init_func=init_animation, interval=1000/fps, save_count=frame_count_estimate, blit=True, repeat=False)

if save_video: 
    if save_as_gif:
        ani.save(video_file+".gif", writer="pillow", dpi=fig.dpi, fps=fps)
    else:
        ani.save(video_file+".mp4", writer="ffmpeg", dpi=fig.dpi, fps=fps)
else:
    plt.show()