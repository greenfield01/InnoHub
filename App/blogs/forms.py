from flask_wtf import Form
from wtforms import (StringField, SubmitField, validators, FileField,
                     ValidationError, TextAreaField, IntegerField, SelectField)

from App.models.posts import Post


class PostForm(Form):
    title = StringField('Title', [validators.DataRequired(
        message="Title field cannot be empty")])
    content = TextAreaField(
        'Content', [validators.DataRequired(message="Content field is required")])
    min_to_read = IntegerField('Minutes to read', validators.DataRequired(
        message="Enter the min to read the post"))
    category = SelectField("Category", coerce=int)
    post_image = FileField(
        'Image', [validators.InputRequired('A post must have an image')])
    submit = SubmitField("Add Post")

    def validate_title(self, title):
        post = Post.query.filter_by(title=title.data).first()
        if post:
            raise ValidationError(
                f"A post with the title {self.title} already exists")


class UpdatePostForm(Form):
    title = StringField('Title', [validators.DataRequired(
        message="Title field cannot be empty")])
    content = TextAreaField(
        'Content', [validators.DataRequired(message="Content field is required")])
    min_to_read = IntegerField('Minutes to read', validators.DataRequired(
        message="Enter the min to read the post"))
    post_image = FileField(
        'Image', [validators.InputRequired('A post must have an image')])
    update = SubmitField("Update Post")

    def validate_title(self, title):
        post = Post.query.filter_by(title=title.data).first()
        if title.data == post.title:
            raise ValidationError(f"A post with same title alread exists")
