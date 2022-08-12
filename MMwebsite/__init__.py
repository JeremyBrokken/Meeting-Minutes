from flask import Flask #for jinja ect..
from flask_sqlalchemy import SQLAlchemy #for databse operations
from os import path #import path module
from flask_login import LoginManager

db = SQLAlchemy() #new database DEFINITION
DB_NAME = "database.db" #database name = ~~

def create_app():
    #initializes flask
    app = Flask(__name__) #__name__ = represenets name of the file
    app.config['SECRET_KEY'] = 'hOgWaRtS98#' # encript or secure the cookies and session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'# tell flask we use database and its location (using SQLite3) [only work in Pythion 3.6 and above = fstring]
    db.init_app(app) #initialize database, by giving it the flask app (take database (defined) tell it this is the app we are going to use with this database)

    # Import blueprints
    from .views import views #import views vairable from the views folder
    from .auth import auth #import auth vairable from the auth folder
   
    #register the imported blueprints
    app.register_blueprint(views, url_prefix='/') # dont define prefix, so accesses all in file without difining eache element
    app.register_blueprint(auth, url_prefix='/')# same as views
    
    # we import this (models). So we load this file and runs before we initialize and run our database.
    from .models import User, Note # >> potentially not possible, guy had issues, says he usually does IT THAT WAY THOUGH SO.. >>"import .models as models" = (also works same- in this situation) If done this way "as models" is because can reference starting with a "." ie .models
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    #Tells flask how to load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #query.get looks by default for primary key
    
    return app

def create_database(app):
    if not path.exists('MMwebsite/' + DB_NAME): # use path module to determine wether our database exists
        db.create_all(app=app) # Pass app because, = if doesnt exist = create it. Need to tell Flask SQLAlchemy which app to create a database for. Also because this app also SQLALCHEMY_DATABASE_URI which says where to create the database 
        print('Created Database!')