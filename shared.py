from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, abort, make_response, json, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
