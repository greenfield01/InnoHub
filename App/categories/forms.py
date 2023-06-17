from flask_wtf import Form
from wtforms import (StringField, SubmitField, validators)


class CategoryForm(Form):
    """This class defines fields for Category page
    Parameter:
        Form: A flask_wtf Object
    """
    name = StringField(
        'Name', [validators.InputRequired('Category name cannot be empty')])
    submit = SubmitField('Submit')
