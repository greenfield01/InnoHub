from App.extensions import (Blueprint, redirect, render_template, url_for, current_user,
                            current_app, secrets, path, getenv,
                            login_required, logout_user, login_user, request, flash, bcrypt, secure_filename)
from App.models.users import User
from App.users.forms import LoginForm, SigupForm, UpdateProfileForm, ResetPasswordForm, ResetRequestForm, ChangePasswordForm
from App.models.innovations import Innovation
from App.innovatioins.forms import InnovationForm
from App.models.categories import Category

import utils


users = Blueprint("users", __name__)

# Individual user route


@users.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    """This route render the all innovations posted by a user
       paramenter:
         user_id (int) : the user Id of the post.
    """
    user_post = Innovation.query.join(User).filter_by(id=user_id).all()
    user = User.query.filter_by(id=user_id).first()
    return render_template('users/user_innovations.html', title='', posts=user_post, user=user)

# Sign up route


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    """This route render the sign up page and register user upon successfull validation of user inputs"""
    form = SigupForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(form.username.data, form.email.data,
                    hash_password, form.phoneNumber.data, form.country.data)
        user.insert()
        flash("Signup successfull", "success")
        return redirect(url_for('users.login'))

    return render_template('users/signup.html', title='Sign Up', form=form)

# Login route


@users.route('/login', methods=['GET', 'POST'])
def login():
    """This route render the loging page and log in the user
    upon validation of the rquired fields.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('users.dashboard'))
        flash("Email/Password is invalid", "danger")
    return render_template('users/login.html', title='Login', form=form)

# Dashboard route


@users.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    """This route upon successfull login, redirectst the user to his/her dashboard"""
    form = InnovationForm(request.form)
    categories = Category.query.all()
    form.category.choices = [(cat.id, cat.name)
                             for cat in Category.query.all()]
    user_posts = Innovation.query.join(User).filter(
        User.id == current_user.id).order_by(Innovation.created_on.desc()).all()
    print(user_posts)
    if request.method == 'POST' and form.validate():
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename != "":
            random_hex = secrets.token_hex(8)
            f_ext = path.splitext(filename)[1]
            if f_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                flash("File format not allowed", "danger")
                return redirect(url_for('dashboard'))
            img_name = random_hex + f_ext
            file.save(path.join(getenv('UPLOAD_PATH'), img_name))
            innovation = Innovation(name=form.title.data, description=form.description.data,
                                    image_url=img_name, user_id=current_user.id,
                                    category_id=form.category.data)
            innovation.inser()
            flash("New innovation successfully added", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("No file selected", "danger")
            return redirect(url_for('users.dashboard'))

    return render_template("users/dashboard.html", title="Dashboard", form=form,
                           categories=categories, posts=user_posts)

# Edit route


@users.route('/dashboard/edit_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    """This route render the edit profile page of user who has been successfully log in."""
    form = UpdateProfileForm(request.form)
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST' and form.validate():
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename != "":
            random_hex = secrets.token_hex(8)
            f_ext = path.splitext(filename)[1]
            if f_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                flash("File format not allow", "danger")
                return redirect(url_for('users.user_profile'))
            img_name = random_hex + f_ext
            file.save(path.join(getenv('UPLOAD_PATH'), img_name))
            user.username = form.username.data
            user.email = form.email.data
            user.picture = img_name
            user.update()
            flash("Profile successfully updated", "success")
            return redirect(url_for('users.dashboard'))
        else:
            user.username = form.username.data
            user.email = form.email.data
            user.update()
            flash("Profile successfully updated withouth Image", "success")
            return redirect(url_for('users.user_profile'))
    else:
        ...
    return render_template("users/user_profile.html", form=form, title="Update Profile")


# reset password route
@users.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    """This route render the reset password page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = ResetRequestForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        utils.send_reset_email(user)
        flash("An email has been sent with instruction to reset your password", "info")
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title="Reset Password", form=form)


# reset password route
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """This route render the password reset page upon successfull verification of sent token
    parameter:
         token (string): sequences of random characters generated using JWT"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hash_pwd
        user.update()
        flash("Your password has been updated, you can now login", "success")
        return redirect(url_for('users.login'))
    return render_template('users/reset_password.html', title='New Password', form=form)


# Change password route
@users.route('/dashboard/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """This route render the change password page from the user dashboard"""
    form = ChangePasswordForm(request.form)
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST' and form.validate():
        if bcrypt.check_password_hash(user.password, form.current_password.data):
            user.password = bcrypt.generate_password_hash(
                form.new_password.data).decode("utf-8")
            user.update()
            flash("Password successfully changed", "success")
            return redirect(url_for('users.change_password'))
        else:
            flash("Current password is invalid", "danger")
            return redirect(url_for('users.change_password'))
    return render_template('users/change_password.html', form=form, title='Change Password')


# Logout route
@users.route('/logout')
@login_required
def logout():
    """This route logout the user from the app"""
    logout_user()
    return redirect(url_for('main.home'))
