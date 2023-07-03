from flask import Flask
from App.extensions import (db, csrf, bcrypt, mail, jwt,
                            login_manager, cors, migrate, ma, getenv)
import config


login_manager.login_view = "login"
login_manager.login_message_category = "info"


def create_app(config=config.Config):
    """A factory function for creating apps"""

    app = Flask(__name__)

    # Settinng of configuration variables
    app.config.from_object(config)
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']
    app.config['UPLOAD_PATH'] = 'static/images/uploads'

    bcrypt.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)
    ma.init_app(app)
    csrf.init_app(app)

    # importing defined blueprints
    from App.errors.handlers import errors
    from App.api.v1.routes import api
    from App.categories.routes import cat
    from App.innovations.routes import innovation
    from App.main.routes import main
    from App.users.routes import users
    from App.blogs.routes import post

    # Registering Blueprints
    app.register_blueprint(errors)
    app.register_blueprint(api, url_prefix="/api/v1")
    app.register_blueprint(cat)
    app.register_blueprint(innovation)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(post)

    return app
