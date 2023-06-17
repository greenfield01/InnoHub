from App.extensions import (
    db, login_manager, UserMixin, Column, String, Integer, relationship, jwt, ma, datetime, environ)


@login_manager.user_loader
def load_user(user_id):
    """This function defines the load user used of logging users
    Parameter:
        user_id (int): The user Id
    Return:
        User: queried from the database
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """This class defines the User model fields
    Parameter:
        db.Model: an instances of SQLAlchemy
        UserMixin: use for the purposer of logging
    """
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
        """This defines the init method
        Parameters:
            username (string): The user name
            email (strin): the user email
            password (string): The password of the user
            phoneNUmber (string): User phone number
            Country (string): user country of origin
        """
        self.username = username
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.country = country

    def insert(self):
        """This function insert new user into the database"""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """This function updates user details in the database"""
        db.session.commit()

    def delete(self):
        """This function delete user from the database"""
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """This function retuens formatted output of user details"""
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
        """This function create a reset token
        Parameter:
            expires (int): Expiry time of the token, default = 1800
        Reurns:
            token: generated token to be sent to user"""
        return jwt.encode({'user_id': self.id, 'exp': expires}, key=environ.get('SECRET_KEY'))

    @staticmethod
    def verify_reset_token(token):
        """This function verify the sent token
        Parameter:
            token: token generated from the get_reset_tokenn function
        Return:
            User
        """
        try:
            user_id = jwt.decode(token, key=environ.get('SECRET_KEY'))[
                'user_id']
        except:
            return None
        return User.query.get(user_id)


class UserSchema(ma.Schema):
    """This class defines the User schema for fetching data"""
    class Meta:
        fields = ('id', 'username', 'email', 'phoneNumber',
                  'country', 'date_registered')
        model = User


# Instantiating the user schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
