from App.extensions import Blueprint

cat = Blueprint("cat", __name__)


@cat.route('/categories', methods=['GET', 'POST'])
def categories():
    ...
