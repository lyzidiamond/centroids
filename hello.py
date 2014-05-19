import os
import json
import shapely
from shapely.geometry import shape, mapping
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['js', 'json', 'geojson'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      file_type = filename.rsplit('.', 1)[1]
      file_title = filename.rsplit('.', 1)[0]
      return redirect(url_for('upload_success', filetype = file_type, filetitle=file_title))
  return '''
  <title>Upload New File</title>
  <body>
  <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file>
      <input type=submit value=Upload>
    </p>
  </form></body>
  '''

@app.route('/uploads/<filetype>/<filetitle>')
def upload_success(filetype, filetitle):
  filename = filetitle + '.' + filetype
  return 'You uploaded ' + filetitle + ', a ' + filetype + ' file. To download, click <a href="' + url_for('download_file', filename=filename) + '">here</a>. To download a feature collection of centroids, click <a href="' + url_for('calculate_centroid', filename = filename) + '">here</a>.'

@app.route('/uploads/centroid/<filename>')
def calculate_centroid(filename):

  file_title = filename.rsplit('.', 1)[0]
  centroids_name = file_title + '_centroids.geojson'
  CENTROID_PATH = './uploads/' + centroids_name
  POLYGONS_PATH = './uploads/' + filename

  feature_collection = {
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

  with open(CENTROID_PATH, 'w') as out:
    out.write(json.dumps(feature_collection))

  return send_from_directory(app.config['UPLOAD_FOLDER'], centroids_name, as_attachment=True, attachment_filename=centroids_name)

@app.route('/uploads/download/<filename>')
def download_file(filename):
  print(filename)
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True, attachment_filename=filename)

app.run(debug=True)