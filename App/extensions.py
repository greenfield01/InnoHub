
import secrets
from os import environ, path, getenv
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user, logout_user
from flask import (Flask, Blueprint, render_template, url_for,
                   redirect, request, flash, jsonify, json, abort, current_app)
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


# Instantiating of Flask app and other packages imported
db = SQLAlchemy()
csrf = CSRFProtect()
bcrypt = Bcrypt()
mail = Mail()
cors = CORS()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()
login_manager = LoginManager()
