import math
import json
from datetime import datetime
import requests

BASE_URL = 'https://stanlytrack3.dfs.de/stanlytrack3/JeCARS/fan/dfs/datasets/GERMANY/flights/st/sum'
BASE_PARAMS = {
  'size': 50,
  'Airport': 'EDDP',
  'Area': 'GERMANY',
}
BASIC_AUTH = 'Basic R0VSTUFOWW46ZmFub21vcw==' # aus den requests von der Webseite ablesen (Inhalt des 'Authorization' headers)

FROM_DATE = datetime(2020, 11, 30, 00, 00)
TO_DATE = datetime(2020, 12, 6, 00, 00)

def fetch_data(from_n=1, fastcount=False):
  params = {
    **BASE_PARAMS,
    'fromTrackDate': FROM_DATE.isoformat(),
    'toTrackDate': TO_DATE.isoformat(),
    'from': from_n,
  }
  if fastcount:
    params['mode'] = 'fastcount'
  headers = {
    'Authorization': BASIC_AUTH,
  }
  r = requests.get(BASE_URL, params=params, headers=headers)
  return r.json()

body = fetch_data(fastcount=True)
total = body['jsonroot']['totalAc']

print(f'{total} total flights to fetch')

all_flights = []

for i in range(0, math.ceil(total / BASE_PARAMS['size'])):
  data = fetch_data(from_n=i * 50 + 1)
  flights = data['jsonroot']['acList']['flights']
  print(f'fetched {len(flights)} flights')
  all_flights.extend(flights)

print('all flights fetched')

bounds_x = [11.842693, 12.742693]
bounds_y = [51.158857, 51.558857]

def in_bounds(coord):
  if coord['x'] < bounds_x[0] or coord['x'] > bounds_x[1]:
    return False
  if coord['y'] < bounds_y[0] or coord['y'] > bounds_y[1]:
    return False
  return True

def cut_coordinates(flight):
  flight_copy = flight.copy()
  flight_copy['track']['plot'] = [coord for coord in flight['track']['plot'] if in_bounds(coord)]
  return flight_copy 

data_cut = [cut_coordinates(flight) for flight in all_flights]

print('flight data cut to bounds')

with open('flight_data.json', 'w') as f:
  json.dump(data_cut, f)
