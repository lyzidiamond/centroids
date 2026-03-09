import os
import json
from io import BytesIO
import shapely
from shapely.geometry import shape, mapping
from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
import requests

ALLOWED_EXTENSIONS = set(['js', 'json', 'geojson'])

app = Flask(__name__)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_centroids(polygons_json):

  feature_collection = {
    'type': 'FeatureCollection',
    'features': []
  }

  for feature in json.loads(polygons_json)['features']:
    feature_geom = shape(feature['geometry'])
    feature_centroid = feature_geom.centroid
    centroid = mapping(feature_centroid)
    feature['geometry'] = centroid
    feature_collection['features'].append(feature)

  return feature_collection

@app.route('/', methods=['GET', 'POST'])
def operation():
  if request.method == 'POST':
    file = request.files['file']
    
    if file and allowed_file(file.filename):

      filename = secure_filename(file.filename)
      file_type = filename.rsplit('.', 1)[1]
      file_title = filename.rsplit('.', 1)[0]

      polygons_json = file.read().decode('utf-8')
      
      byte_stream = BytesIO()
      byte_stream.write(json.dumps(get_centroids(polygons_json)).encode('utf-8'))
      byte_stream.seek(0)

      centroids_filename = file_title + "_centroids.geojson"

      return send_file(byte_stream, download_name=centroids_filename, as_attachment=True)

  return render_template('index.html')

@app.route('/centroids', methods=['POST'])
def api_centroids():
  return jsonify(get_centroids(request.get_data(as_text=True)))

@app.route('/dc-and-utah-20m.json')
def download_file():
  url = 'https://raw.githubusercontent.com/lyzidiamond/centroids/main/examples/dc-and-utah-20m.json'
  filename = 'dc-and-utah-20m.json'
  response = requests.get(url)
  with open(filename, 'wb') as f:
      f.write(response.content)
  return send_file(filename, download_name=filename, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)
