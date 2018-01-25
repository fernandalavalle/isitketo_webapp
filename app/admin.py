import flask
from google.appengine.api import users

import food

app = flask.Flask(__name__)


@app.route('/api/admin/add', methods=['POST'])
def api_add_food():
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
    food.put(f)
    return flask.redirect('/%s' % f.key.string_id())


@app.route('/admin/add_food')
def add_food():
    user = users.get_current_user()
    return flask.render_template(
        'add_food.html', page_title='Add food', nickname=user.nickname())
