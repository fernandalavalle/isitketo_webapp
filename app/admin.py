import flask
from google.appengine.api import users

import food

app = flask.Flask(__name__)


@app.route('/api/admin/add', methods=['POST'])
def api_add_food():
    title = flask.request.form.get('title')
    short_description = flask.request.form.get('short-description')
    description = flask.request.form.get('description')
    rating = int(flask.request.form.get('rating'))

    f = food.Food(
        title=title,
        short_description=short_description,
        description=description,
        rating=rating)
    f.key = food.name_to_key(title)
    f.put()
    return flask.redirect('/%s' % f.key.string_id(), 203)


@app.route('/admin/add_food')
def add_food():
    user = users.get_current_user()
    return flask.render_template(
        'add_food.html', page_title='Add food', nickname=user.nickname())
