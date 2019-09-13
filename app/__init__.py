from flask import Flask
from flask_cors import CORS
from app.controllers import route_handler


app = Flask(__name__)
cors = CORS(app)
route_handler(app)