import os
from dotenv import load_dotenv

load_dotenv()

print(load_dotenv())


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
        os.getenv('DB_USER'), os.getenv('DB_PWD'),
        'localhost:5432', os.getenv('DB_NAME')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
