from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_login import LoginManager, UserMixin
from sqlalchemy import Column, ForeignKey, String, Text, Integer
from sqlalchemy.orm import relationship
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

import jwt
import os


db_name = 'alx_project'
db_path = 'postgresql://{}@{}/{}'.format(
    "postgres:ufazbng", 'localhost:5432', db_name)

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
ma = Marshmallow()

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
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)
    ma.init_app(app)
    
   


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(60), nullable=False, unique=True)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    phoneNumber = Column(String(21), nullable=False)
    country = Column(String(25), nullable=False)
    picture = Column(String(60), nullable=True, default="defaul.png")
    date_registered = Column(String, nullable=True, default=datetime.now)
    innovation = relationship("Innovation", backref="user", lazy=True)

    def __init__(self, username, email, password, phoneNumber, country):
        self.username = username
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.country = country
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phoneNumber': self.phoneNumber,
            'country': self.country,
            'date_registered': self.date_registered
        }
    
    # def __repr__(self):
    #     return f"User({self.username}, {self.email}, {self.country}, {self.date_registered})"

    def get_reset_token(self, expires=1800):
        
        return jwt.encode({'user_id':self.id, 'exp':expires}, key=os.environ.get('SECRET'))
    
    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, key=os.environ.get('SECRET_KEY'))['user_id']
        except:
            return None
        return User.query.get(user_id)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'phoneNumber', 'country', 'date_registered')
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)



class Category(db.Model, UserMixin):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_on = Column(String, nullable=True, default=datetime.now)
    innovation = relationship("Innovation", backref="category", lazy=True)

    def __init__(self, name):
        self.name = name
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit(self)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f"Category({self.name} created on {self.created_on})"
    
class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'created_on')
        model = Category
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)



class Innovation(db.Model, UserMixin):
    __tablename__ = "innovations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text(), nullable=False)
    image_url = Column(String(60), nullable=False)
    created_on = Column(String, nullable=True, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    def __init__(self, name, description, image_url, user_id, category_id):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.user_id = user_id
        self.category_id = category_id
    
    def inser(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.update(self)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Innovation({self.name}, {self.description}, {self.created_on})"
    

class InnovationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Title', 'description', 'image_url', 'created_on', 'username', 'Category Name')
        model = Innovation
innovation_schema = InnovationSchema()
innovations_schema = InnovationSchema(many=True)