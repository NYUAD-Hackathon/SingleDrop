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
class User(Base):

    __tablename__ = 'user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    phone = db.Column(db.String(15),  nullable=False)

    blood_type = db.Column(db.String(3),  nullable=False)

    city = db.Column(db.String(128),  nullable=False)
    neighborhood = db.Column(db.String(128),  nullable=False)

    lat = db.Column(db.Float,  nullable=False)
    lon = db.Column(db.Float,  nullable=False)

    # Authorisation Data: role & status
    #role     = db.Column(db.SmallInteger, nullable=False)
    #status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password, phone, blood_type, city, neighborhood, lat, lon):

        self.name         = name
        self.email        = email
        self.password     = password
        self.phone        = phone
        self.blood_type   = blood_type
        self.city         = city
        self.neighborhood = neighborhood
        self.lat          = lat
        self.lon          = lon

    def __repr__(self):
        return '<User %r>' % (self.name)
