from App.extensions import (Blueprint, request, render_template, current_app, path, flash, abort,
                            redirect, url_for, current_user, secure_filename, secrets, login_required)
from App.models.posts import Post
from App.models.users import User
from App.models.categories import Category
from App.blogs.forms import PostForm, UpdatePostForm


post = Blueprint('post', __name__)


@post.route('/posts', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(User).order_by(
        Post.created_on.desc()).paginate(page=page, per_page=5)
    return render_template('posts/index.html', posts=posts, title='Blog')


@post.route('/post/add', methods=['GET', 'POST'])
@login_required
def store():

    form = PostForm(request.form)
    form.category.choices = [(cat.id, cat.name)
                             for cat in Category.query.all()]
    if request.method == 'POST' and form.validate():
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename != "":
            random_hex = secrets.token_hex(8)
            f_ext = path.splitext(filename)[1]
            if f_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                flash("File format not allowed", "danger")
                return redirect(url_for('post.user_posts'))
            img_name = random_hex + f_ext
        post = Post(user_id=current_user.id, cat_id=form.category.data, title=form.title.data,
                    content=form.content.data, min_to_read=form.min_to_read.data, post_image=img_name)
        post.insert()
        flash("New post successfully added", "success")
        return redirect(url_for("post.get"))
    return render_template('posts/store.html', title='Add Post')


@post.route('/post/show/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show(post_id):
    form = UpdatePostForm(request.form)
    if request.method == 'GET':
        post = Post.query.filter_by(id=post_id).join(User).first()
    elif request.method == 'POST' and form.validate():
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename != "":
            random_hex = secrets.token_hex(8)
            f_ext = path.splitext(filename)[1]
            if f_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                flash("File format not allowed", "danger")
                return redirect(url_for('post.show'))
            img_name = random_hex + f_ext
            post.title = form.title.data
            post.content = form.content.data
            post.min_to_read = form.min_to_read.data
            post.category = form.category.data
            post.post_image = img_name
            post.update()
            flash("Post successfully updated", "success")
            return redirect(url_for('post.show'))
    return render_template("posts/user_post.html", title="My Post", posts=post, form=form)


@post.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).first()
        if post:
            post.delete()
            flash("Post Successfully deleted", "success")
            return redirect(url_for('post.show'))
        else:
            abort(404)


@post.route('/user_posts', methods=['GET', 'POST'])
@login_required
def user_posts():
    form = PostForm(request.form)
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        posts = Post.query.join(User).filter_by(
            User.id == current_user.id).order_by(Post.created_on.desc()).paginate(page=page, per_page=2)
    elif request.method == 'POST':
        ...
    return render_template('user_post.html', form=form, posts=posts, title='Blog Posts')
