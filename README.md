Centroids as a Service
==========

This application reads a valid GeoJSON `FeatureCollection` and returns a valid GeoJSON `FeatureCollection` of centroids.

In the output:

* All properties are retained.
* Polygon features become points that represent the polygon's centroid.
* LineString features become points that represent the middle of the LineString.
* Point features do not change.
* MultiPolygon handling depends on Shapely centroid behavior.

This is a [Flask](https://flask.palletsprojects.com/en/stable/) application that uses the [Shapely](https://shapely.readthedocs.io/en/stable/) Python library.
The service can be accessed in two ways: an upload/download page and a web service.
The application is currently [deployed to Render](https://centroids.onrender.com).

## Why would anyone use this?

I originally wrote this app in 2014 as a way to understand how to write a Flask app and deploy it to Heroku. I didn't touch it again until 2026, when I modernized the app to current conventions and redeployed it to Render (RIP Heroku, I'll miss you forever, bless you Render, I'm enjoying using you). I'm once again using this as a practice project to understand how to build and deploy apps in 2026.

In 2014, I found this app useful to create labels for polygons. (Of course, sometimes the centroid falls outside of the polygon and you have to adjust it -- there are other geospatial operations that can guarantee the point ends up inside the bounds of the polygon.) Nowadays, labeling engines are far more robust and helpful than they were 12 years ago, so this use case isn't as applicable.

The ultimate use case for centroids is _simplification_. You can calculate the rough distance between two cities by using the centroids as reference points. You can use centroids as a tool for certain clustering algorithms, like K-means.

This app is also pretty straightforward with minimal code. It would require few steps to change it to use a different operation. What a great way to explore Shapely!

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
}' https://centroids.onrender.com/centroids
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
