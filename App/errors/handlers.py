from App.extensions import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(403)
def forbiddeen(error):
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(501)
def server_error(error):
    return render_template("errors/501.html"), 501
