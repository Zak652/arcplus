import os
from arm import app

def run():
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port = port)

if __name__ == '__main__':
	run()