import sys
import gzip
import shapefile
from shapely.geometry import shape, Point
import numpy as np

shp = shapefile.Reader('geofiles/nybb_15c/nybb_wgs84.shp')
shapes = [shape(shp.shape(i)) for i in range(shp.numRecords)]
counts = np.zeros(shp.numRecords, dtype='int')

tweet_count = 0

for line in gzip.open("NYC.json.gz"):
    try:
        tweet = eval(line.strip())
        point = None

        tweet_count += 1

        if tweet_count % 100 == 0:
            print(tweet_count, file=sys.stderr)

        if "coordinates" in tweet and tweet["coordinates"] is not None:
            point = Point(tweet["coordinates"]["coordinates"])
        else:
            if "place" in tweet and tweet["place"]["bounding_box"] is not None:
                bbox = shape(tweet["place"]["bounding_box"])
                point = bbox.centroid

        if point is not None:
            for borogh in range(shp.numRecords):
                if shapes[borogh].contains(point):
                    counts[borogh] += 1
                    break
    except:
        pass

fp_out = open("NYC_counts.csv", "w")

print("id,name,count", file=fp_out)
for borogh in range(shp.numRecords):
    record = shp.record(borogh)
    print(",".join([str(record[0]), record[1], str(counts[borogh])]), file=fp_out)

fp_out.close()
