from flask import Flask
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1:project1@localhost/userprofile"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://jidcyardqkevbd:884df959cb8a28e37c10268bbf4ecc32fa735cab14f0aa57b7822025dad332c9@ec2-184-73-216-48.compute-1.amazonaws.com:5432/dbf3vajn92grau"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

UPLOAD_FOLDER = './app/static/uploads'

db = SQLAlchemy(app)

# Flask-Login login manager
#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
