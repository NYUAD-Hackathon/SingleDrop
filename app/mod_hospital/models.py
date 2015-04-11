# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class Hospital(Base):

    __tablename__ = 'hospital'

    # User Name
    name    = db.Column(db.String(128),  nullable=False,
                                         unique = True)

    # Identification Data: email & password
    #email    = db.Column(db.String(128),  nullable=False,
    #                                        unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Location
    city = db.Column(db.String(128), nullable=False)
    neighborhood = db.Column(db.String(128), nullable=False)

    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)


    # New instance instantiation procedure
    #def __init__(self, name, email, password):
    def __init__(self, name, password, city, neighbourhood, lat, lon):

        self.name     = name
        #self.email    = email
        self.password = password
        self.city = city
        self.neighbourhood = neighbourhood
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<User %r>' % (self.name)