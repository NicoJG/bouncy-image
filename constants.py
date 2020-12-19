# video constants
save_video = False
save_as_gif = True
video_file = "video" # without ending
video_height = 720 # pixels (if it's to low, you get an error)

# figure constants
fig_height = 1000 # Inches (don't change! the less it is the less precise is the marker_size)
marker_size_correction_factor = 1 # workaround if the marker size is not correct

# animation constants
animation_start_delay = 2 # how many seconds the animation should stand still at the beginning
animation_time = 10 # how many seconds should the animation run
animation_end_delay = 2 # how many seconds the animation should stand still at the end
fps = 30 # frames per second
fixed_dt = save_video # when saved as a video you'll want a fixed dt
show_debug_time = False

# image constants
image_path = "images/tu.png"
image_height = 32 # how many pixels should be displayed in a vertical line? The width is calculated from this
crop_image = True # should the image be cropped to the important part?
filter_white_pixels = True # If too much of your image is missing you may want to make the background transparent and make this False

# ball constants
r = 0.35 # radius
v_min = 5 # min velocity
v_max = 10 # max velocity

# collision constants
sector_max_size = 3 # max length of the sides of the sector