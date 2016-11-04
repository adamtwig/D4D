import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#load CSV data
data = np.genfromtxt("../output/heatmap/SET2_P01-season.csv", delimiter=',',  dtype=None, names=True, missing='NaN')

heatmap, xedges, yedges = np.histogram2d(data['1'], data['2'])
plt.imshow(heatmap)
'''
ax = fig.add_subplot(133)
ax.set_title('NonUniformImage: interpolated')
im = mpl.image.NonUniformImage(ax, interpolation='bilinear')
xcenters = xedges[:-1] + 0.5 * (xedges[1:] - xedges[:-1])
ycenters = yedges[:-1] + 0.5 * (yedges[1:] - yedges[:-1])
im.set_data(xcenters, ycenters, H)
ax.images.append(im)
ax.set_xlim(xedges[0], xedges[-1])
ax.set_ylim(yedges[0], yedges[-1])
ax.set_aspect('equal')

plt.savefig('./heatmap_plot.png')
'''
