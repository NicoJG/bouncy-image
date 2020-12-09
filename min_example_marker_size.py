import matplotlib.pyplot as plt
from numpy import pi

# check out: https://stackoverflow.com/questions/65174418/how-to-adjust-the-marker-size-of-a-scatter-plot-so-that-it-matches-a-given-radi

n = 16
# create a n x n square with a marker at each point as dummy data
x_data = []
y_data = []
for x in range(n):
    for y in range(n):
        x_data.append(x)
        y_data.append(y)

# open figure
fig,ax = plt.subplots(figsize=[7,7])
# set limits BEFORE plotting
ax.set_xlim((0,n-1))
ax.set_ylim((0,n-1))
# radius in data coordinates:
r = 0.5 # units
# radius in display coordinates:
r_ = ax.transData.transform([r,0])[0] - ax.transData.transform([0,0])[0] # points
# strange correction factor
correction_factor = 0.5
# marker size as the area of a circle
marker_size = (2*r_)**2 * correction_factor
# plot
ax.scatter(x_data, y_data, s=marker_size, edgecolors='black')

plt.show()