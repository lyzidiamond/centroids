from os import environ

from hello import app

app.run(port=environ.get('PORT', 5000))
