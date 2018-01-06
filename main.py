import logging

import flask
from google.appengine.ext import ndb

import food

app = flask.Flask(__name__)


def find_food(food_name):
    key = ndb.Key(food.Food, food_name)
    return key.get()


@app.route('/')
def root():
    return 'Welcome to isitketo! Search to find out if a food is keto-friendly.'


@app.route('/<food_name>')
def check_food(food_name):
    f = find_food(food_name)
    return '%s: %s' % (f.title, f.description)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
