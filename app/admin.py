import flask
from google.appengine.api import users

import food
import main

app = flask.Flask(__name__)


def _update_food_from_form(food):
    food.brand = flask.request.form.get('brand')
    food.title = flask.request.form.get('title')
    food.variety = flask.request.form.get('variety')
    food.short_description = flask.request.form.get('short-description')
    food.description = flask.request.form.get('description')
    food.has_image = flask.request.form.get('has-image') != None

    if (flask.request.form.get('rating')):
        food.rating = int(flask.request.form.get('rating'))
    return food


@app.route('/api/admin/add', methods=['POST'])
def api_add_food():
    f = _update_food_from_form(food.Food())
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
    f = food.find_by_name(food_name)
    f = _update_food_from_form(f)
    f = food.update(food_name, f)
    return flask.redirect('/%s' % f.key.string_id())


@app.route('/admin/edit/<food_name>')
def edit_food(food_name):
    f = food.find_by_name(food_name)
    if f:
        user = users.get_current_user()
        name = food.food_to_name(f)
        return flask.render_template(
            'food_form.html',
            page_title=('Edit food - %s' % name),
            nickname=user.nickname(),
            food_name=name,
            food=f)
    else:
        return main.render_unknown_food(food_name)
