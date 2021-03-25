from datetime import datetime
import json 
import itertools
from operator import itemgetter

# [height (m), dezibel] values for a medium haul flight when taking off
takeoff = [
  [250, 100.5], [500, 94.5], [1000, 87.5], [1500, 83], [2000, 79.5], [2500, 77],[3000, 74],
  [3500, 72], [4000, 70], [4500, 68], [5000, 66], [5500, 64], [6000, 62.5], [6500, 60.75],
  [7000, 59.5], [7500, 58], [8000, 56.5], [8500, 55], [9000, 53.5]
]
# [height (m), dezibel]  values for a medium haul flight when landing
landing = [
  [250, 85.5], [500, 79.5], [1000, 72.5], [1500, 68], [2000, 64.5], [2500, 62],
  [3000, 59], [3500, 57], [4000, 55], [4500, 53], [5000, 51], [5500, 49]
]

bounds_x = [11.842693, 12.742693]
bounds_y = [51.158857, 51.558857]

def ft_to_m(height):
  return round(height / 3.2808)

def linear_interp(c1, c2, x):
  x1, y1 = c1
  x2, y2 = c2
  return y1 + ((y2 - y1) / (x2 - x1)) * (x - x1)

def noise(height, starting):
  values = takeoff if starting else landing
  low = next((e for e in values if e[0] <= height), values[0])
  high = next((e for e in values if e[0] >= height), values[-1])
  if low == high:
    return low[1]
  return round(linear_interp(low, high, height))

def geojson_point(point, time, starting):
  return { 
    'type': 'Feature',
    'geometry': {'type': 'Point', 'coordinates': [point['x'], point['y']]},
    'properties': {
      'time': datetime.fromtimestamp(time / 1000).isoformat(),
      'height': ft_to_m(point['z']),
      'noise': noise(ft_to_m(point['z']), starting),
      'starting': starting,
    }
  }

def geojson_features(flight):
  if flight['From_Abbr'] == 'LEJ' and flight['To_Abbr'] == 'LEJ':
    return []
  if flight['From_Abbr'] == 'LEJ' or flight['To_Abbr'] == 'LEJ':
    return [
      geojson_point(p, flight['Time'], flight['From_Abbr'] == 'LEJ')
      for p in flight['track']['plot']]
  return []

def geojson_collection(features):
  return {
    'type': 'FeatureCollection',
    'features': features
  }

data = json.load(open('data/flight_data.json'))

features = list(itertools.chain(
  *[geojson_features(f) for f in data]
))

feature_map = {
  'starting': {},
  'landing': {},
}

max_diff = 0.0001

def is_redundant_point(key, point_coords, noise):
  if not feature_map[key][noise]:
    return False
  for coords in feature_map[key][noise]:
    x_diff = abs(point_coords[0] - coords[0])
    if x_diff <= max_diff:
      y_diff = abs(point_coords[1] - coords[1])
      if y_diff <= max_diff:
        return True
  return False

filtered_features = []

for feature in features:
  noise, starting = itemgetter('noise', 'starting')(feature['properties'])
  coords = feature['geometry']['coordinates']
  key = 'starting' if starting else 'landing'
  if noise not in feature_map[key]:
    feature_map[key][noise] = [coords]
  elif not is_redundant_point(key, coords, noise):
    feature_map[key][noise].append(coords)
    del feature['properties']['starting']
    filtered_features.append(feature)

geojson = {
  'type': 'FeatureCollection',
  'features': filtered_features
}

with open('data/geojson_nolocal_2/all_week.geojson', 'w') as f:
  json.dump(geojson_collection(filtered_features), f)

def is_weekday_day(isodate):
  date = datetime.fromisoformat(isodate)
  return 2 <= date.isoweekday() <= 4 and 7 <= date.hour <= 22

with open('data/geojson_nolocal_2/weekdays_day.geojson', 'w') as f:
  json.dump(geojson_collection([p for p in filtered_features if is_weekday_day(p['properties']['time'])]), f)

def is_weekday_night(isodate):
  date = datetime.fromisoformat(isodate)
  return 1 <= date.isoweekday() <= 5 and (date.hour >= 21 or date.hour <= 8)

with open('data/geojson_nolocal_2/weekdays_night.geojson', 'w') as f:
  json.dump(geojson_collection([p for p in filtered_features if is_weekday_night(p['properties']['time'])]), f)

def is_weekend(isodate):
  date = datetime.fromisoformat(isodate)
  return 6 <= date.isoweekday() <= 7

with open('data/geojson_nolocal_2/weekend.geojson', 'w') as f:
  json.dump(geojson_collection([p for p in filtered_features if is_weekend(p['properties']['time'])]), f)
