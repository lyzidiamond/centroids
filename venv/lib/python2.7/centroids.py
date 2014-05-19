import json
import shapely
from sys import argv
from shapely.geometry import shape, mapping

def centroids(input_file, output_file):

  POLYGONS_PATH = str(input_file)
  OUTPUT_PATH = str(output_file)

  feature_collection =  {
    'type': 'FeatureCollection',
    'features': []
  }

  polygons_json = open(POLYGONS_PATH).read()
  for feature in json.loads(polygons_json)['features']:
    feature_geom = shape(feature['geometry'])
    feature_centroid = feature_geom.centroid
    centroid = mapping(feature_centroid)
    feature['geometry'] = centroid
    feature_collection['features'].append(feature)

  with open(OUTPUT_PATH, 'w') as out:
    out.write(json.dumps(feature_collection))