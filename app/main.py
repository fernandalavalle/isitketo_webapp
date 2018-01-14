import logging

import flask
from google.appengine.ext import ndb

import food

_SITE_TITLE = 'Is It Keto?'

app = flask.Flask(__name__)


def find_food(food_name):
    key = ndb.Key(food.Food, food_name)
    return key.get()


@app.route('/')
def root():
    return flask.render_template('index.html', page_title=_SITE_TITLE)


@app.route('/<food_name>')
def check_food(food_name):
    f = find_food(food_name)
    if f:
        return flask.render_template(
            'food.html',
            key=f.key.string_id(),
            page_title=('%s - %s' % (f.title, _SITE_TITLE)),
            title=f.title,
            rating=f.rating,
            short_description=f.short_description,
            description=f.description)
    else:
        return flask.render_template(
            'unknown_food.html',
            title=food_name,
            page_title=_SITE_TITLE,
            short_description='We\'re not sure')


@app.route('/favicon.ico')
def favicon():
    flask.abort(404)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
