import json
import math
import numpy as np
import pandas as pd

data = json.load(open('data/geojson_nolocal_2/weekend.geojson'))

min_x, max_x = (11.842693, 12.742693)
min_y, max_y = (51.158857, 51.558857)

x_scale = 150
interval = (max_x - min_x) / x_scale
y_scale = math.ceil((max_y - min_y) / interval)

x_coords = []
y_coords = []
noises = [[[] for _ in range(y_scale)] for _ in range(x_scale)]

for feature in data['features']:
  x, y = feature['geometry']['coordinates']
  x_index = int((x - min_x) // interval)
  y_index = int((y - min_y) // interval)
  noises[x_index][y_index].append(feature['properties']['noise'])

features = []

def create_feature(coords, noise):
  return {
    'type': 'Feature',
    'geometry': {
      'type': 'Polygon',
      'coordinates': [coords]
    },
    'properties': {
      'noise': noise
    }
  }

for x in range(x_scale):
  for y in range(y_scale):
    x_pos = x * interval + min_x
    y_pos = y * interval + min_y
    coords = [
      [x_pos, y_pos],
      [x_pos + interval, y_pos],
      [x_pos + interval, y_pos + interval],
      [x_pos, y_pos + interval],
    ]
    # mean_noise = max(50, sum(noises[x][y]) / max(len(noises[x][y]), 1))
    # features.append(create_feature(coords, mean_noise))
    max_noise = max([50] + noises[x][y])
    features.append(create_feature(coords, max_noise))

geojson = {
  'type': 'FeatureCollection',
  'features': features
}

with open('data/geojson_raster/raster-fine_max_weekend.geojson', 'w') as f:
  json.dump(geojson, f)
