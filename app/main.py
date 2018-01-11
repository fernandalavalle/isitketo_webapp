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
    return flask.render_template('index.html')


@app.route('/<food_name>')
def check_food(food_name):
    f = find_food(food_name)
    if f:
        return flask.render_template(
            'food.html',
            key=f.key.string_id(),
            title=f.title,
            description=f.description)
    else:
        return flask.render_template(
            'food.html',
            title=food_name,
            description=
            'Hmm, I dunno if that\'s keto... Check back in a bit and I\'ll probably know.'
        )


@app.route('/favicon.ico')
def favicon():
    flask.abort(404)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
