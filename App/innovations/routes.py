from App.extensions import Blueprint, request, render_template
from App.models.innovations import Innovation
from App.models.users import User

innovation = Blueprint("innovation", __name__)

# Innovations route


@innovation.route('/innovations', methods=['GET', 'POST'])
def innovations():
    """This route render all innovations posted by users with pagination"""
    page = request.args.get('page', 1, type=int)
    all_post = Innovation.query.join(User).order_by(
        Innovation.created_on.desc()).paginate(page=page, per_page=2)
    return render_template('innovations/innovations.html', title="InnoHub", posts=all_post)
