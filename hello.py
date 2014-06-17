import os
import json
import StringIO
import shapely
from shapely.geometry import shape, mapping
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['js', 'json', 'geojson'])

app = Flask(__name__)

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

      polygons_json = file.read()
      
      strIO = StringIO.StringIO()
      strIO.write(json.dumps(get_centroids(polygons_json)))
      strIO.seek(0)

      centroids_filename = file_title + "_centroids.geojson"

      return send_file(strIO, attachment_filename=centroids_filename, as_attachment=True)

  return '''
  <title>Upload New File</title>
  <body>
    <div id="header">
      <h1>Centroids!</h1>
      <h2>This application reads a valid geojson file and returns a valid geojson file of centroids.</h2>
    </div>
    <div id="notes">
      <p>In the resulting file:</p>
      <ul>
        <li>All properties are retained in the output file.</li>
        <li>Polygon features become points that represent the Polygon's centroid.</li>
        <li>LineString features become points that represent the middle of the LineString.</li>
        <li>Point features do not change.</li>
        <li>I have no idea how this handles MultiPolygons.</li>
      </ul>
    </div>
    <div id="form">
      <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
          <input type=submit value=Make centroids>
        </p>
      </form>
    </div>
    <div id="footer">
      <p>This is a Flask application that uses the Shapely Python library. It was made by <a href="http://twitter.com/lyzidiamond">Lyzi Diamond</a>. <a href="http://github.com/lyzidiamond/centroids">It is on GitHub.</a></p>
    </div>
  </body>
  '''
