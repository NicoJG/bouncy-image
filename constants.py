# video constants
save_video = True
save_as_gif = True
video_file = "video" # without ending
video_height = 1080 # pixels

# figure constants
fig_height = 10 # Inches (don't change! it messes with the resolution for saved videos)
fig_dpi = video_height/fig_height
show_axis = False
marker_size_correction_factor = 0.45 # just try it out with r=0.5 and "guess" the right factor

# animation constants
animation_start_delay = 2 # how many seconds the animation should stand still at the beginning
animation_time = 10 # how many seconds should the animation run
animation_end_delay = 2 # how many seconds the animation should stand still at the end
fps = 30 # frames per second
fixed_dt = True # when saved as a video you'll want a fixed dt
show_debug_time = False

# image constants
image_path = "images/python_logo_64.png"

# ball constants
r = 0.35 # radius
v_min = 5 # min velocity
v_max = 10 # max velocity

# collision constants
sector_max_size = 3 # max length of the sides of the sector