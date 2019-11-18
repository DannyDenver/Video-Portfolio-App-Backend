import os

from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_path = os.environ["DATABASE_URL"]


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Videographer(db.Model): 
    __tablename__ = 'videographer'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    location = db.Column(db.String(30))
    bio = db.Column(db.String())
    profile_url = db.Column(db.String())
    videos = db.relationship("Video", backref=db.backref("videographer"), lazy="dynamic", cascade="delete")


    @hybrid_property
    def current_videos(self):
        return self.videos.all()


    def __init__(self, first_name, last_name, location, bio, profile_url):
        self.first_name = first_name
        self.last_name = last_name
        self.location = location
        self.bio = bio
        self.profile_url = profile_url


    def __repr__(self):
        return '<Videographer id: {0}, name: {1} {2}, location: {3} >'.format(self.id, self.first_name, self.last_name, self.location)


    def short(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'location': self.location,
            'profilePictureUrl': self.profile_url
        }


    def long(self):
        return {
            'id': self.id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'location': self.location,
            'bio': self.bio,
            'profilePictureUrl': self.profile_url,
            'videos': [vd.serialize() for vd in self.current_videos]            
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()


    def update(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Video(db.Model):
    __tablename__ = 'video'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    videographer_id = db.Column(db.Integer, db.ForeignKey('videographer.id'), nullable=False)
    url = db.Column(db.String())
    title = db.Column(db.String(200))
    description = db.Column(db.String())


    def __init__(self, videographer_id, url, title, description):
        self.videographer_id = videographer_id
        self.url = url
        self.title = title
        self.description = description


    def __repr__(self):
        return '<Video id: {0}, title: {1} >'.format(self.id, self.title)


    def serialize(self):
        return {
            'id': self.id,
            'videographer_id': self.videographer_id,
            'url': self.url,
            'title': self.title,
            'description': self.description
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
