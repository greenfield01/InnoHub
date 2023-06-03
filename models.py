from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin


from flask_cors import CORS
from flask_migrate import Migrate

db_name = 'flask_blog'
db_path = 'postgresql://{}@{}/{}'.format(
    "postgres:ufazbng", 'localhost:5432', db_name)

# Instance of SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()


def setup_db(app, database_path=db_path):
    """
    setup_db(app):
        bind flask application and SQLAlchemy serve
    app: flask instance
    database_path: string - path to db
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """Defines a User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    image_path = Column(String(120), nullable=True, default='default.png')
    created_at = Column(String, nullable=True, default=datetime.utcnow)
    posts = relationship('Post', backref="author", lazy=True)

    def __init__(self, username, email, password):
        self.id = self.id
        self.username = username
        self.email = email
        self.password = password

    def insert(self):
        """Insert a new user"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """A function that updates the user"""
        db.session.commit()

    def delete(self):
        """A function that deletes a user"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.created_at})"


class Post(db.Model, UserMixin):
    """A class that defines Post schema"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False)
    description = Column(Text, nullable=False)
    post_date = Column(String, nullable=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, title, description, user_id):
        self.id = self.id
        self.title = title
        self.description = description
        self.user_id = user_id

    def insert(self):
        """A function that insert a new post"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """A function that update a given post"""
        db.session.commit()

    def delete(self):
        """A function that deletes a post"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Post({self.title}, {self.description}, {self.post_date}, {self.user_id})"
