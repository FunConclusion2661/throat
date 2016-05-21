""" Database table definitions """

from sqlalchemy import Column, Integer, String, Text, DateTime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """ Basic user data (Used for login or password recovery) """
    uid = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(128), unique=True)
    # In case we migrate to a different cipher for passwords
    # 1 = bcrypt
    crypto = Column(Integer)
    password = Column(String)
    # Account status
    # 0 = OK; 1 = banned; 2 = shadowbanned?; 3 = sent to oblivion?
    status = Column(Integer)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.crypto = 1
        self.status = 0

        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def __repr__(self):
        return '<User %r>' % self.username


class Sub(db.Model):
    """ Basic sub data """
    sid = Column(Integer, primary_key=True)  # sub id
    name = Column(String(32), unique=True)  # sub name
    title = Column(String(128))  # sub title

    status = Column(Integer)  # Sub status. 0 = ok; 1 = banned; etc
    
    def __init__(self, name, title):
        self.name = name
        self.title = title

    def __repr__(self):
        return '<Sub {0}-{1}>'.format(self.name, self.title)


class SubPost(db.Model):
    """ Represents a post on a sub """
    pid = Column(Integer, primary_key=True)  # post id
    sid = Column(Integer)  # sub id

    uid = Column(Integer)  # post author
    title = Column(String(128))  # post title
    link = Column(String(128))  # post target (if it is a link post)
    content = Column(Text)  # post content (if it is a text post)

    posted = Column(DateTime)

    def __repr__(self):
        return '<SubPost {0} (In Sub{1})>'.format(self.title, self.sid)
