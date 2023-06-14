# Import of flask packages
from flask import Flask, render_template, url_for, redirect, request, flash, jsonify, json, abort
from forms import LoginForm, SigupForm, InnovationForm,\
     CategoryForm, UpdateProfileForm, ChangePasswordForm, ResetRequestForm, ResetPasswordForm
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user, logout_user
from os import environ, path, urandom
from models import setup_db, User, Innovation, Category, login_manager,\
     user_schema, users_schema, categories_schema, category_schema, innovation_schema, innovations_schema
import secrets
from flask_jwt_extended import JWTManager

# Instantiating of Flask app and other packages imported
app = Flask(__name__)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Settinng of configuration variables
app.config['SECRET_KEY'] = environ.get('SECRET')
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.flv', '.gifv', '.webm']
app.config['UPLOAD_PATH'] = 'static/images/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = environ.get('MAIL_USER')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PWD')
mail = Mail(app)
jwt = JWTManager(app)

setup_db(app=app)

# The home/index route
@app.route('/home')
@app.route('/')
def home():
   """This route render the home or index page of the application"""
   return render_template('home.html', title='InnoHub')

# Innovations route
@app.route('/innovations', methods=['GET', 'POST'])
def innovations():
     """This route render all innovations posted by users with pagination"""
     page = request.args.get('page', 1, type=int)
     all_post = Innovation.query.join(User).order_by(Innovation.created_on.desc()).paginate(page=page, per_page=2)
     return render_template('innovations.html', title="InnoHub", posts=all_post)

# Individual user route
@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
     """This route render the all innovations posted by a user
        paramenter:
          user_id (int) : the user Id of the post.
     """
     user_post = Innovation.query.join(User).filter_by(id=user_id).all()
     user = User.query.filter_by(id=user_id).first()
     return render_template('user_innovations.html', title='', posts=user_post, user=user)

@app.route('/categories', methods=['GET', 'POST'])
def categories():
        ...

# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """This route render the sign up page and register user upon successfull validation of user inputs"""
    form = SigupForm(request.form)
    if request.method == 'POST' and form.validate():
         hash_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
         user = User(form.username.data, form.email.data, hash_password, form.phoneNumber.data, form.country.data)
         user.insert()
         flash("Signup successfull", "success")
         return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """This route render the loging page and log in the user
    upon validation of the rquired fields.
    """
    if current_user.is_authenticated:
         return redirect(url_for('home'))

    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate():
         user = User.query.filter_by(email=form.email.data).first()
         if user and bcrypt.check_password_hash(user.password, form.password.data):
              login_user(user)
              next_page = request.args.get("next")
              return redirect (next_page) if next_page else redirect(url_for('dashboard'))
         flash("Email/Password is invalid", "danger")
    return render_template('login.html', title='Login', form=form)

# Dashboard route
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
     """This route upon successfull login, redirectst the user to his/her dashboard"""
     form = InnovationForm(request.form)
     categories = Category.query.all()
     form.category.choices = [(cat.id, cat.name) for cat in Category.query.all()]
     user_posts = Innovation.query.join(User).filter(User.id == current_user.id).order_by(Innovation.created_on.desc()).all()
     print(user_posts)
     if request.method == 'POST' and form.validate():
          file = request.files['file']
          filename = secure_filename(file.filename)
          if filename != "":
               random_hex = secrets.token_hex(8)
               f_ext = path.splitext(filename)[1]
               if f_ext not in app.config['UPLOAD_EXTENSIONS']:
                    flash("File format not allowed", "danger")
                    return redirect(url_for('dashboard'))
               img_name = random_hex + f_ext
               file.save(path.join(app.config['UPLOAD_PATH'], img_name))
               innovation = Innovation(name=form.title.data, description=form.description.data,\
                                       image_url=img_name, user_id = current_user.id,\
                                        category_id=form.category.data)
               innovation.inser()
               flash("New innovation successfully added", "success")
               return redirect(url_for('dashboard'))
          else:
               flash("No file selected", "danger")
               return redirect(url_for('dashboard'))

     return render_template("dashboard.html", title="Dashboard", form=form,\
                            categories=categories, posts=user_posts)
# Edit route
@app.route('/dashboard/edit_profile', methods=['GET', 'POST'])
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
               if f_ext not in app.config['UPLOAD_EXTENSIONS']:
                    flash("File format not allow", "danger")
                    return redirect(url_for('user_profile'))
               img_name = random_hex + f_ext
               file.save(path.join(app.config['UPLOAD_PATH'], img_name))
               user.username = form.username.data
               user.email = form.email.data
               user.picture = img_name
               user.update()
               flash("Profile successfully updated", "success")
               return redirect(url_for('dashboard'))
          else:
               user.username = form.username.data
               user.email = form.email.data
               user.update()
               flash("Profile successfully updated withouth Image", "success")
               return redirect(url_for('user_profile')) 
     else:
          ...
     return render_template("user_profile.html", form=form, title="Update Profile")

# send email function
def send_reset_email(user):
     """This functions sends a reset password link to user email
     parameter:
          user: user object
     """
     token = user.get_reset_token()
     msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
     msg.body = f'''To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}

IF you did not make this request then simply ignore it and no changes will be made
'''
     mail.send(msg)

# reset password route
@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
     """This route render the reset password page"""
     if current_user.is_authenticated:
          return redirect(url_for('dashboard'))

     form = ResetRequestForm(request.form)
     
     if request.method == 'POST' and form.validate():
          user = User.query.filter_by(email=form.email.data).first()
          send_reset_email(user)
          flash("An email has been sent with instruction to reset your password", "info")
          return redirect(url_for('login'))
     return render_template('reset_request.html', title="Reset Password", form=form)

# reset password route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
     """This route render the password reset page upon successfull verification of sent token
     parameter:
          token (string): sequences of random characters generated using JWT"""
     if current_user.is_authenticated:
          return redirect(url_for('dashboard'))
     
     user = User.verify_reset_token(token)
     if user is None:
          flash("That is an invalid or expired token", "warning")
          return redirect(url_for('reset_request'))
     form = ResetPasswordForm(request.form)
     if request.method == 'POST' and form.validate():
          hash_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
          user.password = hash_pwd
          user.update()
          flash("Your password has been updated, you can now login", "success")
          return redirect(url_for('login'))
     return render_template('reset_password.html', title='New Password', form=form)


# Change password route
@app.route('/dashboard/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
     """This route render the change password page from the user dashboard"""
     form = ChangePasswordForm(request.form)
     user = User.query.filter_by(id=current_user.id).first()
     if request.method == 'POST' and form.validate():
          if bcrypt.check_password_hash(user.password, form.current_password.data):
               user.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
               user.update()
               flash("Password successfully changed", "success")
               return redirect(url_for('change_password'))
          else:
               flash("Current password is invalid", "danger")
               return redirect(url_for('change_password'))
     return render_template('change_password.html', form=form, title='Change Password')

# Logout route
@app.route('/logout')
@login_required
def logout():
     """This route logout the user from the app"""
     logout_user()
     return redirect(url_for('home'))



##################################################
#                 API's Section                  #
##################################################

# A contanct that defines the numbers of items per page, 5
PER_PAGE = 5

def paginate(request, selection):
     """This function defines a pagination handler.
     parameters:
          request: The request object
          selection: The collection object
     Return:
          current_items: A section of the collection indicated by the start & end
     """
     page = request.args.get('page', 1, type=int)
     start = (page - 1) * PER_PAGE
     end = start + PER_PAGE
     result = [item.format() for item in selection]
     current_items = result[start : end]
     return current_items


# Get users route
@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """This route returns all users of the appliation
    Return: 
          User details in JSON format
    """
    try:
     users = User.query.all()
     
     return jsonify({
          'status': 'Ok',
          'message': 'success',
          'count': len(users),
          'data': users_schema.dump(users)
     })
    except:
         abort(400)
     

# Get User route
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
     """This route returns specific user from the appliation
     parameter:
          user_id (int): The user Id
     Return:
          if found,User details in JSON format, otherwise, abort with 404 response
     """
     try:
         user = User.query.filter_by(id=user_id).first()
         if user:
               return jsonify(
                    {
                         'status': 'Ok',
                         'message': 'success',
                         'data': user_schema.dump(user)
                         }
                    )  
         else:
              abort(404)   
     except:
         abort(404)



# Categories route
@app.route('/api/v1/categories')
def get_categories():
     """This route returns all innovation categories used in the appliation
     Return:
          if found,categories details in JSON format, otherwise, abort with 400 response
     """
     
     try:
          categories = Category.query.all()
          return jsonify(
               {
                    'status': 200,
                    'message': 'success',
                    'count': len(categories),
                    'data': categories_schema.dump(categories)
               }
          )
     except:
          abort(400)


# Get Category route
@app.route('/api/v1/categories/<int:cat_id>')
def get_category(cat_id):
    """This route returns specific category from the appliation
     parameter:
          user_id (int): The category Id
     Return:
          if found, category details in JSON format, otherwise, abort with 404 response
     """
    try:
         category = Category.query.filter_by(id=cat_id).first()

         if category:
               return jsonify(
                    {
                         'status': 200,
                         'message': 'success',
                         'data': category_schema.dump(category)
                    }
               )
         else:
              abort(404)
    except:
         abort(404)

# Innovations route
@app.route('/api/v1/innovations', methods=['GET', 'POST'])
def get_innovations():
     """This route returns all innovations posted in the appliation
     Return:
          Innovation details in JSON format
     """
     try:
     #     innovations = Innovation.query.join(Innovation.user_id == User.id).join(Innovation.category_id == Category.id).all()
         innovations = Innovation.query.join(User).join(Category).\
          with_entities(Innovation.id, Innovation.name.label('Title'), Innovation.description,\
                        Innovation.created_on, User.username, Category.name.label('Category Name')).all()
         return jsonify(
              {
                   'status code': 200,
                   'message': 'success',
                   'count': len(innovations),
                   'data': innovations_schema.dump(innovations)
              }
         )
     except:
         abort(400)

# Get specific Innovation route
@app.route('/api/v1/innovations/<int:id>', methods=['GET', 'POST'])
def get_innovation(id):
     """This route returns specific innovation from the appliation
     parameter:
          user_id (int): The Innovation Id
     Return:
          if found, Innovation details in JSON format, otherwise, abort with 404 response
     """
     try:
         innovation = Innovation.query.join(User).join(Category).filter_by(Innovation.id == id).first()
         print(innovation)
         result = innovation.filter_by(id).first()
         print(result)
         if innovation:
              
               return jsonify(
                    {
                         'status code': 200,
                         'message': 'success',
                         'data': innovation_schema.dump(result)
                    }
               )
         else:
              abort(404)
     except:
         abort(400)

# 404 error handler
@app.errorhandler(404)
def not_found(error):
     """This function handles 'Not found error' 
     parameter:
          error: error code
     """
     return jsonify(
          {
          'success': False,
          'message': 'Not found'
          }
     ), 404

# 400 error handler
@app.errorhandler(400)
def bad_request(error):
     """This function handles 'Forbidden error' 
     parameter:
          error: error code
     """
     return jsonify(
          {
               'success': False,
               'message': 'Bad request'
          }
     ), 400


# Start of the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)