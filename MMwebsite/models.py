# to be for, databse models for users and notes(to be minutes)
# A database model is a layout or a blueprint for an object that is going to be stored in the database, ie [database] all Notes or Users gotta look like this
#sql language = me happy :)
from . import db #importing from __init__.py db.[ from . = from this package, anything in __init__.py]
from flask_login import UserMixin # first use of module. Custom class inherited to give user object things specific for flask_login
from sqlalchemy.sql import func #dont need to specify date field. Lets sqlalchemy do it for me. Every new note auto add date for me.

class Minute(db.Model): 
    id = db.Column(db.Integer, primary_key=True) #by default, add new object id, auto selecte[auto increment] = do not need to set
    topic = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #defaults = autodate
    dateCompletion = db.Column(db.String(10000))
    raisedBy = db.Column(db.String(50))
    absentees = db.Column(db.String(100))
    actionBy = db.Column(db.String(50))
    required = db.Column(db.String(1000))
    information  = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key relationsip. Must be same [integer]. One to many relationship. Keeps notes to users. ForeignKey = user.id[databasefolder.column]lower case u
#additional note relationsip trypes are one-to-one, one-to-many and many-to-one. Im using one-to-many =needs relationship key

class User(db.Model, UserMixin): # inherit from db.Model + user object only inherits from UserMixin
    #defining a schema or layout for some object that can be stored in the database
    id = db.Column(db.Integer, primary_key=True) #primary key
    email = db.Column(db.String(150), unique=True) #cannot create another user with the same email
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # tells flask and sqlalchemy = add to this relationship Notes id. relationship capitol N