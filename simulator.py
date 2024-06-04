import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from math import asin, atan2, cos, degrees, radians, sin , sqrt


app = Flask(__name__)
CORS(app)


def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d / R) + cos(lat1) * sin(d / R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d / R) * cos(lat1), cos(d / R) - sin(lat1) * sin(lat2)
    )
    return (
        degrees(lat2),
        degrees(lon2),
    )


base_locarion=[51.385785,35.687527]

locations=[]
base_bearing=-30
for column_index in range(5):
    col_loc=get_point_at_distance(base_locarion[0],base_locarion[1],d=column_index/150,bearing=base_bearing+180)
    for row_index in range(5):
        locations.append(get_point_at_distance(col_loc[0],col_loc[1],d=row_index/150,bearing=base_bearing+270))
    



@app.route('/get_data', methods=['GET'])
def simulated_data():
   data=[]
   for _ in range(random.randint(1,20)):
      loc=random.choice(locations)
      accuracy=random.random()
      data.append(
         {
            "type": "Feature",
            "geometry": {
                    "type": "Point",
                    "coordinates": [loc[0], loc[1]]
            },
            "properties": {
                    "accuracy":accuracy,
                    "radius":(1-accuracy)*30,
            }
        }
      )
      
      
   
   return jsonify(data)

if __name__ == '__main__':
   app.run(port=9090)