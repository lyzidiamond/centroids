Centroids!
==========

This application reads a valid GeoJSON `FeatureCollection` and returns a valid GeoJSON `FeatureCollection` of centroids.

In the output:

* All properties are retained.
* Polygon features become points that represent the polygon's centroid.
* LineString features become points that represent the middle of the LineString.
* Point features do not change.
* MultiPolygon handling depends on Shapely centroid behavior.

This is a Flask application that uses the Shapely Python library.
The service can be accessed in two ways: an upload/download page and a web service.

## Web service

POST GeoJSON to `/centroids`.

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d \
'{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [-80.93490600585938, 35.263561862152095],
          [-80.69320678710938, 35.32745068492882],
          [-80.60531616210938, 35.14124815600257],
          [-80.83328247070312, 35.06597313798418],
          [-80.93490600585938, 35.263561862152095]
        ]]
      }
    }
  ]
}' http://127.0.0.1:5000/centroids
```

## Running locally (Python 3)

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
python runserver.py
```

Then open http://127.0.0.1:5000/.

## Deploying on Render

This repo includes `render.yaml` for Blueprint deploys.

1. Push this repo to GitHub.
2. In Render, click **New +** → **Blueprint**.
3. Connect the repo and deploy.

Render will:

* install dependencies with `pip install -r requirements.txt`
* run the app with `gunicorn hello:app`
* use Python `3.12.2`
