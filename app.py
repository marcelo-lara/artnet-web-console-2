import asyncio
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from lib.fixtures import async_setup_artnet


## Setup WEB server ########################################################################
app = Flask(__name__, template_folder='html_templates')
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


## Setup ArtNet ############################################################################
with app.app_context():
    asyncio.run(async_setup_artnet('config/fixtures.yaml'))


## Main loop ##############################################################################
if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)