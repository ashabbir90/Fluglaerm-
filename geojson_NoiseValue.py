from sys import argv

from os.path import exists
import json 

script, in_file, out_file = argv

data = json.load(open(in_file))

# bounding box coordinates
#                  [longitude, latitude ]
north_west_point = [11.834589, 51.542230]
south_east_point = [12.789278, 51.141833]

# Punkte
geojson = {
    "type": "FeatureCollection",
    "features": [
        { 
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [p["x"], p["y"]]},
            "properties": {
                "Time": d["Time"],
                "height": round(p["z"]/3.2808),
                "noise": round((p["z"]/3.2808) * (-0.00773876404494382) + 77.75561797752809)
            }
        } for d in data for p in d["track"]["plot"] if ((p["y"] <= north_west_point[1]) & (p["y"] >= south_east_point[1]) & (p["x"] <= south_east_point[0]) & (p["x"] >= north_west_point[0]))
    ]
}
output = open(out_file, 'w')
json.dump(geojson, output)