Centroids!
==========

This application reads a valid geojson file and returns a valid geojson file of centroids.

In the resulting file:

* All properties are retained in the output file.
* Polygon features become points that represent the Polygon's centroid.
* LineString features become points that represent the middle of the LineString.
* Point features do not change.
* I have no idea how this handles MultiPolygons.

This is a [Flask](http://flask.pocoo.org/) application that uses the [Shapely](https://github.com/Toblerity/Shapely) Python library by @sgillies. Issues and pull requests welcome!

## Running locally

1. Optionally create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

```
virtualenv venv
source venv/bin/activate
```

1. Install [requirements](https://devcenter.heroku.com/articles/python-pip)

```
pip install -r requirements.txt
```

1. Start the server

```
python hello.py
```

You should now be able to visit the application at http://127.0.0.1:5000/.

## Notes

To run on Heroku requires a third party `BUILDPACK` for Heroku
