import logging
import re

import flask
from google.appengine.ext import ndb

import auth_manager
import email_validator
import food
import subscriber

_SITE_TITLE = 'Is It Keto?'

app = flask.Flask(__name__)


def find_food(food_name):
    key = _food_name_to_key(food_name)
    return key.get()


def _food_name_to_key(food_name):
    key = food_name.lower()
    key = re.sub(r'[^a-z]', '-', key)
    return ndb.Key(food.Food, key)


def _sanitize_food_name(food_name):
    return re.sub(r'[^a-zA-Z\-\.\s&*\+:0-9]', '', food_name)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.route('/')
def root():
    return flask.render_template('index.html', page_title=_SITE_TITLE)


@app.route('/api/subscribe', methods=['POST'])
def add_subscriber():
    email = flask.request.form.get('email')
    if not email_validator.validate(email):
        raise InvalidUsage('Invalid email address')
    food_name = flask.request.form.get('food-name')
    if not food_name:
        raise InvalidUsage('Invalid food name')
    s = subscriber.SubscriberModel(email=email, food_name=food_name)
    s.put()
    return flask.jsonify({'success': True})


@app.route('/api/admin/add', methods=['POST'])
def api_add_food():
    if not auth_manager.is_request_authorized(flask.request):
        logging.warning('Unauthorized attempt to access add API')
        flask.abort(403)
    title = flask.request.form.get('title')
    short_description = flask.request.form.get('short-description')
    description = flask.request.form.get('description')
    rating = int(flask.request.form.get('rating'))

    f = food.Food(
        title=title,
        short_description=short_description,
        description=description,
        rating=rating)
    f.key = _food_name_to_key(title)
    f.put()
    return flask.redirect('/%s' % f.key.string_id(), 203)


@app.route('/<food_name>')
def check_food(food_name):
    food_name = _sanitize_food_name(food_name)
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
            short_description='We\'re not sure',
            load_js=True)


@app.route('/favicon.ico')
def favicon():
    flask.abort(404)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
