from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
myapp = Flask(__name__)
myapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopdata.db'
myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
myapp.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet('photos', IMAGES)
configure_uploads(myapp, photos)

myapp.secret_key = 'SECRET KEY'

db = SQLAlchemy(myapp)
bcrypt = Bcrypt(myapp)
search = Search()
search.init_app(myapp)

migrate = Migrate(myapp, db)
with myapp.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(myapp, db, render_as_batch=True)
    else:
        migrate.init_app(myapp, db)

login_manager = LoginManager()
login_manager.init_app(myapp)
login_manager.login_view = "CustomerLogin"
login_manager.needs_refresh_message_category= "danger"
login_manager.login_message = u"Please login first"

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes

