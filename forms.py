from flask_wtf import Form
from wtforms import StringField, PasswordField, EmailField, SelectField, FileField, SubmitField, validators, ValidationError
from models import User, Category
from flask_login import current_user

class SigupForm(Form):
    username = StringField('Username', [validators.InputRequired(message='Username is required')])
    email = EmailField('Email', [validators.InputRequired(message='Email is required')])
    phoneNumber = StringField('Phone Number', [validators.InputRequired(message='Phone number is required')])
    country = StringField('Country', [validators.InputRequired(message="Country is required")])
    password = PasswordField('Password', [validators.InputRequired(message='Password id required'),\
                                          validators.EqualTo('confirm_password', message='Password and confirm password must match')])
    confirm_password = PasswordField('Confirm password')
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already in use, kindly login')

class ChangePasswordForm(Form):
    current_password = PasswordField('Current Password', [validators.InputRequired("Enter current password")])
    new_password = PasswordField('New Password', [validators.InputRequired("Enter new password"), validators.EqualTo('cpassword', message='Password must match')])
    cpassword = PasswordField('Confirm Password')
    submit = SubmitField('Change Password')


class LoginForm(Form):
    email = EmailField('Email', [validators.InputRequired('Email field cannot be empty')])
    password = PasswordField('Password', [validators.InputRequired('Password cannot be empty')])
    submit = SubmitField('Login')

class ResetRequestForm(Form):
    email = EmailField('Email', [validators.InputRequired('Email field cannot be empty')])
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(f"No account for '{email}' in our record.")

class ResetPasswordForm(Form):
    password = PasswordField('Password', [validators.InputRequired(message='Password id required'),\
                                          validators.EqualTo('confirm_password', message='Password and confirm password must match')])
    confirm_password = PasswordField('Confirm password')
    submit = SubmitField('Reset Password')

class UpdateProfileForm(Form):
    username = StringField("Username", [validators.InputRequired(
        message="Username is required"), validators.Length(min=2, max=25, message="Username must be above 2 & not more than 25")])
    email = EmailField(
        "Email", [validators.InputRequired(message="Email field cannot be empty")])
    picture = FileField('Select file', name='file')
    update = SubmitField("Update")

    def validate_username(self, username):
        """Function that validate existance of username"""
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "Username already taken")

    def validate_email(self, email):
        """Function that validates the existance of email"""
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already in use")

class InnovationForm(Form):
    title = StringField('Title', [validators.InputRequired('Innovation title is required')])
    description = StringField('Description', [validators.InputRequired('Innovation description is required')])
    image = FileField('Image', name="file")
    category = SelectField("Category", coerce=int)
    submit = SubmitField('Add')

class CategoryForm(Form):
    name = StringField('Name', [validators.InputRequired('Category name cannot be empty')])
    submit = SubmitField('Submit')

