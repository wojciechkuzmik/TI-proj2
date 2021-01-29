import os

from flask import Flask, current_app


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'RunFaster.sqlite'),
)


try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db
db.init_app(app)

from . import auth
app.register_blueprint(auth.bp)

from . import wall
app.register_blueprint(wall.bp)
app.add_url_rule('/', endpoint='index')
