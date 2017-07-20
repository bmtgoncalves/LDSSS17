import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.collections import PatchCollection
from matplotlib import patches
import shapefile
import numpy as np

shp = shapefile.Reader('geofiles/nybb_15cc/nybb_wgs84.shp')
boros = {}

for shaperecord in shp.iterShapeRecords():
    boro_id = int(shaperecord.record[0])
    parts = list(shaperecord.shape.parts)
    parts.append(len(shaperecord.shape.points))
    boros[boro_id] = []

    for i in range(0, len(parts)-1):
        boros[boro_id].append(patches.Polygon(shaperecord.shape.points[parts[i]:parts[i+1]-1]))

data = {}
line_count = 0

for line in open("NYC_counts.csv"):
    fields = line.strip().split(',')

    line_count += 1

    if line_count == 1:
        header = dict(zip(fields, range(len(fields))))
        continue

    data[int(fields[header["id"]])] = int(fields[header["count"]])

Min = np.min(list(data.values()))
Max = np.max(list(data.values()))
norm = Normalize(vmin=Min, vmax=Max)
cmap = plt.get_cmap('Blues')

patches = []
colors = []

for boro_id in boros.keys():
    patches.extend(boros[boro_id])

    if boro_id in boros:
        colors.extend([cmap(norm(data[boro_id])) for i in range(len(boros[boro_id]))])
    else:
        colors.append([cmap(norm(Min)) for i in range(len(boros[boro_id]))])

fig = plt.figure()
ax = plt.gca()

bbox = shp.bbox
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])
ax.add_collection(PatchCollection(patches, facecolor=colors, edgecolor='k')) #, linewidths=2, zorder=2))

fig.savefig('NYC_counts.png')
plt.close(fig)
