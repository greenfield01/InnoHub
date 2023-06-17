from App.extensions import Blueprint, abort, jsonify
from App.models.users import User, user_schema, users_schema
from App.models.categories import Category, categories_schema, category_schema
from App.models.innovations import Innovation, innovation_schema, innovations_schema

api = Blueprint("api", __name__)


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
    current_items = result[start: end]
    return current_items


# Get users route
@api.route('/users', methods=['GET'])
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
@api.route('/users/<int:user_id>', methods=['GET'])
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
@api.route('/categories')
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
@api.route('/categories/<int:cat_id>')
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


@api.route('/innovations', methods=['GET', 'POST'])
def get_innovations():
    """This route returns all innovations posted in the appliation
    Return:
         Innovation details in JSON format
    """
    try:
        #     innovations = Innovation.query.join(Innovation.user_id == User.id).join(Innovation.category_id == Category.id).all()
        innovations = Innovation.query.join(User).join(Category).\
            with_entities(Innovation.id, Innovation.name.label('Title'), Innovation.description,
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


@api.route('/innovations/<int:id>', methods=['GET', 'POST'])
def get_innovation(id):
    """This route returns specific innovation from the appliation
    parameter:
         user_id (int): The Innovation Id
    Return:
         if found, Innovation details in JSON format, otherwise, abort with 404 response
    """
    try:
        innovation = Innovation.query.join(User).join(
            Category).filter_by(Innovation.id == id).first()
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


@api.errorhandler(404)
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


@api.errorhandler(400)
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
