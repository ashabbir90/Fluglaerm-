import json

# Load flight data
with open('flight_data.json') as f:
  data = json.load(f)

bounds_x = [11.842693, 12.742693]
bounds_y = [51.158857, 51.558857]

def in_bounds(coord):
  if coord['x'] < bounds_x[0] or coord['x'] > bounds_x[1]:
    return False
  if coord['y'] < bounds_y[0] or coord['y'] > bounds_y[1]:
    return False
  return True

def cut_coordinates(flight):
  # Why flight.copy and not just flight
  flight_copy = flight.copy()
  # flight plot (coordinates) = Array | take coord (Aufforderung) for coord (elemnt) in flight (flight object) if in_bounds returns true
  flight_copy['track']['plot'] = [coord for coord in flight['track']['plot'] if in_bounds(coord)]
  return flight_copy # returns it to be saved in data_cut

# data_cut = do (cut_coordinates(flight) for flight (each flight object) in data (json file))
# iterates through data (each flight) and gives it to cut_coordinates
data_cut = [cut_coordinates(flight) for flight in data]

with open('data_cut.json', 'w') as f:
  json.dump(data_cut, f)
