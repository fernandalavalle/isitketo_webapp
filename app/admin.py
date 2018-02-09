import re

import flask
from google.appengine.api import users

import food

app = flask.Flask(__name__)


def _sanitize_food_name(food_name):
    return re.sub(r'[^a-zA-Z\-\.\s&*\+:0-9]', '', food_name)


def _make_food_from_form():
    brand = flask.request.form.get('brand')
    title = flask.request.form.get('title')
    variety = flask.request.form.get('variety')
    short_description = flask.request.form.get('short-description')
    description = flask.request.form.get('description')
    rating = int(flask.request.form.get('rating'))
    has_image = flask.request.form.get('has-image') != None

    f = food.Food(
        brand=brand,
        title=title,
        variety=variety,
        short_description=short_description,
        description=description,
        rating=rating,
        has_image=has_image)

    return f


@app.route('/api/admin/add', methods=['POST'])
def api_add_food():
    f = _make_food_from_form()
    food.put(f)
    return flask.redirect('/%s' % f.key.string_id())


@app.route('/admin/add_food')
def add_food():
    user = users.get_current_user()
    return flask.render_template(
        'food_form.html',
        page_title='Add food',
        nickname=user.nickname(),
        food=None)


@app.route('/api/admin/edit/<food_name>', methods=['POST'])
def api_edit_food(food_name):
    f = _make_food_from_form()
    f = food.update(food_name, f)
    return flask.redirect('/%s' % f.key.string_id())


@app.route('/admin/edit/<food_name>')
def edit_food(food_name):
    user = users.get_current_user()
    food_name = _sanitize_food_name(food_name)
    f = food.find_by_name(food_name)
    if f:
        return flask.render_template(
            'food_form.html',
            page_title=('Edit food - %s' % food_name),
            nickname=user.nickname(),
            food_name=food_name,
            food=f)
