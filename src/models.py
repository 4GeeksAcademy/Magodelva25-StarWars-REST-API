from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=True)
    gravity = db.Column(db.Integer, unique=False, nullable=True)
    activity = db.Column(db.String(20), unique=False, nullable=True)

    def __repr__(self):
        return '<planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity,
            "activity": self.activity
        }

class Characters(db.Model):
    __tablename__='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.String, unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    heigth = db.Column(db.Integer, unique=False, nullable=False)
    affiliation = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return '<characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "age": self.age,
            "heigth": self.heigth,
            "affiliation": self.affiliation
        }
    
class Fav_characters(db.Model):
    __tablename__='fav-characters'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<fav_characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "character": self.character_id,
            "user": self.user_id
            # do not serialize the password, its a security breach
        }

class Fav_planets(db.Model):
    __tablename__='fav-planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, unique=True, nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<fav_planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet_id,
            "user": self.user_id
            # do not serialize the password, its a security breach
        }