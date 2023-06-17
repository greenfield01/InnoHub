from App.extensions import render_template, Blueprint

main = Blueprint("main", __name__)

# The home/index route


@main.route('/home')
@main.route('/')
def home():
    """This route render the home or index page of the application"""
    return render_template('main/home.html', title='InnoHub')
