import json

data = json.load(open('data/flight_data.json'))

collection = []

for flight in data:
  plot = flight['track']['plot']
  if flight['From_Abbr'] == 'LEJ' and flight['To_Abbr'] == 'LEJ':
    continue
  if len(plot) > 0 and (flight['From_Abbr'] == 'LEJ' or flight['To_Abbr'] == 'LEJ'):
    coordinates = [[point['x'], point['y']] for point in plot]
    linestring = {
      'type': 'Feature',
      'properties': {
        'name': flight['Call'],
      },
      'geometry': {
        'type': 'LineString',
        'coordinates': coordinates
      }
    }
    collection.append(linestring)

geojson = {
  'type': 'FeatureCollection',
  'features': collection
}

with open('data/flight_lines.geojson', 'w') as f:
  json.dump(geojson, f)
