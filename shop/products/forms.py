from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, StringField, TextAreaField, validators
from wtforms import Form

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    color = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image_1', validators=[FileAllowed(['.jpg','.png','.gif','.jpeg'])])
    image_2 = FileField('Image_2', validators=[FileAllowed(['.jpg','.png','.gif','.jpeg'])])
    image_3 = FileField('Image_3', validators=[FileAllowed(['.jpg','.png','.gif','.jpeg'])])