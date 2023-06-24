from wtforms import (Form, StringField, SelectField,
                     FileField, SubmitField, validators)


class InnovationForm(Form):
    """This class defines fields for Posting Innovations
    Parameter:
        Form: A flask_wtf Object
    """
    title = StringField(
        'Title', [validators.InputRequired('Innovation title is required')])
    description = StringField(
        'Description', [validators.InputRequired('Innovation description is required')])
    image = FileField('Image', name="file")
    category = SelectField("Category", coerce=int)
    submit = SubmitField('Add')
