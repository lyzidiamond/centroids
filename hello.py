import os
import json
import shapely
import StringIO
from shapely.geometry import shape, mapping
from flask import Flask, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['js', 'json', 'geojson'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def centroid():
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file_type = filename.rsplit('.', 1)[1]
      file_title = filename.rsplit('.', 1)[0]

      feature_collection = {
        'type': 'FeatureCollection',
        'features': []
      }

      polygons_json = file.read()
      for feature in json.loads(polygons_json)['features']:
        feature_geom = shape(feature['geometry'])
        feature_centroid = feature_geom.centroid
        centroid = mapping(feature_centroid)
        feature['geometry'] = centroid
        feature_collection['features'].append(feature)
      strIO = StringIO.StringIO()
      strIO.write(json.dumps(feature_collection))
      strIO.seek(0)
      centroids_filename = file_title + "_centroids.geojson"
      return send_file(strIO, attachment_filename=centroids_filename, as_attachment=True)
  return '''
  <title>Upload New File</title>
  <body>
  <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file>
      <input type=submit value=Upload>
    </p>
  </form></body>
  '''
