import re

import flask
from google.appengine.api import users

import food

app = flask.Flask(__name__)



def _get_food_props_from_form():
    food_props = {}
    food_props['brand'] = flask.request.form.get('brand')
    food_props['title'] = flask.request.form.get('title')
    food_props['variety'] = flask.request.form.get('variety')
    food_props['short_description'] = flask.request.form.get('short-description')
    food_props['description'] = flask.request.form.get('description')
    food_props['rating'] = int(flask.request.form.get('rating'))
    food_props['has_image'] = flask.request.form.get('has-image') != None

    return food_props


@app.route('/api/admin/add', methods=['POST'])
def api_add_food():
    food_props = _get_food_props_from_form()
    food.put(food.update_food_props(food_props, food.Food()))
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
    food_props = _get_food_props_from_form()
    f = food.update(food_name, food_props)
    return flask.redirect('/%s' % f.key.string_id())


@app.route('/admin/edit/<food_name>')
def edit_food(food_name):
    user = users.get_current_user()
    f = food.find_by_name(food_name)
    if f:
        return flask.render_template(
            'food_form.html',
            page_title=('Edit food - %s' % food_name),
            nickname=user.nickname(),
            food_name=food_name,
            food=f)
