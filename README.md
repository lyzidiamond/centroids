Centroids!
==========

This application reads a valid geojson FeatureCollection and returns a valid geojson FeatureColleciton of centroids.

In the output:

* All properties are retained.
* Polygon features become points that represent the Polygon's centroid.
* LineString features become points that represent the middle of the LineString.
* Point features do not change.
* I have no idea how this handles MultiPolygons.

This is a [Flask](http://flask.pocoo.org/) application that uses the [Shapely](https://github.com/Toblerity/Shapely) Python library by [@sgillies](http://github.com/sgillies). Issues and pull requests welcome!

The service can be accessed in two ways: an upload/download page and a web service.

## Upload/download

The upload/download page can be found [here](http://centroids.herokuapp.com). It is pretty self explanatory.

## Web service

The web service lives at http://centroids.herokuapp.com/centroids. You can post to it with geojson.

Here is an example of how you might do that from the command line with `curl` (example from [@invisiblefunnel](http://github.com/invisiblefunnel)):

    $ curl -X POST -H "Content-Type: application/json" -d \
     '{
       "type": "FeatureCollection",
       "features": [
         {
           "type": "Feature",
           "properties": {},
           "geometry": {
             "type": "Polygon",
             "coordinates": [
               [
                 [
                   -80.93490600585938,
                   35.263561862152095
                 ],
                 [
                   -80.69320678710938,
                   35.32745068492882
                 ],
                 [
                   -80.60531616210938,
                   35.14124815600257
                 ],
                 [
                   -80.83328247070312,
                   35.06597313798418
                 ],
                 [
                   -80.93490600585938,
                   35.263561862152095
                 ]
               ]
             ]
           }
         }
       ]
     }' http://centroids.herokuapp.com/centroids
     
Should return:

    {
      "features": [
        {
          "geometry": {
            "coordinates": [
              -80.76829071683488, 
              35.199632857787904
            ], 
            "type": "Point"
          }, 
          "properties": {}, 
          "type": "Feature"
        }
      ], 
      "type": "FeatureCollection"
    }

## Running locally

Optionally create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

```
virtualenv venv
source venv/bin/activate
```

Install [requirements](https://devcenter.heroku.com/articles/python-pip)

```
pip install -r requirements.txt
```

Start the server

```
python hello.py
```

You should now be able to visit the application at http://127.0.0.1:5000/.

## Notes

To run on Heroku requires a third party `BUILDPACK` for Heroku
