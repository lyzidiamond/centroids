from os import environ

from hello import app

if __name__ == '__main__':
	app.run(port=int(environ.get('PORT', 5000)))
