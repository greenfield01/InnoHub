import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
        os.getenv('DB_USER'), os.getenv('DB_PWD'),
        'localhost:5432', os.getenv('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
