import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, redirect, request, flash, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_modals import Modal, render_template_modal
from flask_login import login_required, login_user, logout_user, current_user
from forms import RegistratioinForm, LoginForm, UpdateForm, PostForm, UpdatePostForm
from models import User, Post, setup_db, login_manager


app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)
modal = Modal(app=app)

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()
csrf.init_app(app)
setup_db(app=app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
@app.route('/index')
def index():
    # all_post = Post.query.join(User, Post.user_id == User.id).all()
    page = request.args.get('page', 1, type=int)

    all_post = Post.query.join(User).\
        with_entities(Post.id, Post.title, Post.description, Post.post_date, User.username).\
        order_by(Post.post_date.desc()).paginate(page=page, per_page=2)
    return render_template('home.html', title='Home', posts=all_post)


@app.route('/about')
def about():
    return render_template('about.html', title='About Us')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route for registering users"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistratioinForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        user.insert()
        flash(f'Thank you for registerig', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash("Username/password is invalid", "danger")
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
@login_required
def logout():
    """A route that logout a user"""
    logout_user()
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# def save_file(file):
#     random_hex = secrets.token_hex(8)
#     if allowed_file(file):
#         f_name, f_ext = os.path.splitext(file)
#         picture_name = random_hex + f_ext
#         picture_path = os.path.join(
#             app.root_path, 'static/images', picture_name)

#         output_size = (100, 100)
#         i = Image.open(file)
#         i.thumbnail(output_size)
#         i.save(picture_path)
#     return picture_name


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """A route that renders the dashboard"""
    form = UpdateForm(request.form)
    if request.method == 'POST' and form.validate():
        if 'file' not in request.files:
            flash('No file part', "info")
            return redirect(url_for('dashboard'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', "info")
            return redirect(url_for('dashboard'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, 'static/images', filename))
            user = User.query.filter_by(id=current_user.id).first()
            user.email = form.email.data
            user.username = form.username.data
            user.image_path = filename
            user.update()
            flash("Updated successfuly", "success")
            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', title='Dashboard', form=form, image=current_user.image_path)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    """This route create new post"""
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data,
                    description=form.description.data, user_id=current_user.id)
        post.insert()
        flash("New post successfully added", "success")
        return redirect(url_for('index'))
    elif request.method == 'GET':
        ...
    return render_template('create_post.html', title='New Post', form=form)


@app.route('/show_post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    form = UpdatePostForm(request.form)
    if request.method == 'GET':
        post = Post.query.filter_by(id=post_id).join(User).first()
    elif request.method == 'POST' and form.validate():
        post = Post.query.filter_by(id=post_id).first()
        post.title = form.title.data
        post.description = form['description'].data
        post.update()
        flash("Post successfully updated", "success")
        return redirect(url_for('index'))
    return render_template_modal('show_post.html', title='Show Post', post=post, form=form)


@app.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).first()
        if post:
            post.delete()
            flash("Post successfully deleted", "success")
            return redirect(url_for('index'))
        else:
            abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
