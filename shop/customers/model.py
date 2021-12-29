from shop import db, login_manager
from datetime import  datetime
from flask_login import UserMixin
import json

@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    # f_name = db.Column(db.String(100), unique=False, default='f_name')
    username = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(16), unique=False)
    country = db.Column(db.String(30), unique=False)
    state = db.Column( db.String(30), unique=False)
    city = db.Column(db.String(30), unique=False)
    contact = db.Column(db.String(17), unique=False)
    address = db.Column(db.String(300), unique=False)
    zipcode = db.Column(db.String(50), unique=False)
    profile = db.Column(db.String(50), unique=False, default="profile.jpg")
    date_created = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name

class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(Self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique = False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<CustomerOrder % r>' % self.invoice

db.create_all()
