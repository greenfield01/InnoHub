from App.extensions import (Blueprint, request, render_template, current_app, path, flash, abort,
                            redirect, url_for, current_user, secure_filename, secrets, login_required)
from App.models.posts import Post
from App.models.users import User
from App.models.categories import Category
from App.blogs.forms import PostForm, UpdatePostForm


post = Blueprint('post', __name__)


@post.route('/posts', methods=['GET', 'POST'])
def get():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.join(User).order_by(
        Post.created_on.desc()).paginate(page=page, per_page=5)
    return render_template('posts/posts.html', posts=posts, title='Blog')


@post.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():

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
    return render_template('posts/add_new.html', title='Add Post')


@post.route('/my_posts', methods=['GET', 'POST'])
@login_required
def user_posts():

    posts = Post.query.join(User).filter_by(
        User.id == current_user.id).order_by(Post.created_on.desc()).all()
    return render_template("posts/user_post.html", title="My Post", posts=posts)


@post.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = UpdatePostForm(request.form)
    userPost = Post.query.filter_by(id=post_id).first()
    return render_template('posts/edit_post.html', title='Edit Post', form=form, post=userPost)


@post.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):

    form = UpdatePostForm(request.form)
    userPost = Post.query.filter_by(id=post_id).first()
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
        userPost.title = form.title.data
        userPost.content = form.content.data
        userPost.min_to_read = form.min_to_read.data
        userPost.category = form.category.data
        userPost.post_image = img_name
        userPost.update()
        flash("Post successfully updated", "success")
        return redirect(url_for('post.user_posts'))


@post.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).first()
        if post:
            post.delete()
            flash("Post Successfully deleted", "success")
        else:
            abort(404)
