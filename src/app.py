"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, Fav_characters, Fav_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_get_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))

    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def handle_get_user(id):
    user = User.query.get(id)
    user = user.serialize()

    return jsonify(user), 200

@app.route('/user', methods=['POST'])
def handle_add_user():
   body = request.get_json()
   if "name" not in body:
       return ({ 'msg': 'error name is required'}), 400
   if "email" not in body:
       return ({ 'msg': 'error email is required'}), 400
   if "password" not in body:
       return ({ 'msg': 'error password is required'}), 400

   new_user = User();
   new_user.name = body['name']
   new_user.email = body['email']
   new_user.password = body['password']
   
   db.session.add(new_user)
   db.session.commit()
   
   return jsonify(new_user.serialize()), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def handle_remove_user(id):
    user = User.query.get(id)
    db.session.remove(user)
    db.session.commit()

    return jsonify({}), 204

@app.route('/user/favorites/<int:id>', methods=['GET'])
def get_user_favorites(id):
    all_user_planet_favorites = Fav_planets.query.filter_by(user_id=id)
    all_user_people_favorites = Fav_characters.query.filter_by(user_id=id)

    
    return jsonify({
        "fav_planets": [planet.serialize() for planet in all_user_planet_favorites],
        "fav_people": [people.serialize() for people in all_user_people_favorites]
    }), 200


@app.route('/planets', methods=['GET'])
def handle_get_planets():
    all_planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))

    return jsonify(all_planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def handle_get_planet(id):
    planet = Planets.query.get(id)
    planet = Planets.serialize()

    return jsonify(planet), 200

@app.route('/planets', methods=['POST'])
def handle_add_planet():
   body = request.get_json()

   new_planet = Planets();
   new_planet.name = body['name']
   new_planet.population = body['population']
   new_planet.gravity = body['gravity']
   new_planet.activity = body['activity']
   
   db.session.add(new_planet)
   db.session.commit()
   
   return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:id>', methods=['DELETE'])
def handle_remove_planet(id):
    planet = Planets.query.get(id)
    db.session.delete(planet)
    db.session.commit()

    return jsonify({}), 204

@app.route('/planet/favorites', methods=['GET'])
def get_planet_favorites():
    all_planet_favorites = Fav_planets.query.all()
    return jsonify([planetfavorite.serialize() for planetfavorite in all_planet_favorites]), 200

@app.route('/favorite/planet', methods=['POST'])
def add_planet_favorite():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Request body is missing"}), 400
    
    planet_id = body.get('planet_id')
    user_id = body.get('user_id')

    if not planet_id or not user_id:
        return jsonify({"msg": "planet_id and user_id are required"}), 400

    try:
        favorite = Fav_planets(planet_id=planet_id, user_id=user_id)
        db.session.add(favorite)
        planet = Planets.query.get(planet_id)
        planet_serialize = planet.serialize()

        if planet_serialize["stars"] is None:
            planet.stars = 1
        else:
            planet.stars = planet_serialize["stars"]+1

        
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    favorite = Fav_planets.query.filter_by(planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200



@app.route('/characters', methods=['GET'])
def handle_get_characters():
    all_characters = Characters.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))

    return jsonify(all_characters), 200

@app.route('/characters/<int:id>', methods=['GET'])
def handle_get_character(id):
    character = Characters.query.get(id)
    character = Characters.serialize()

    return jsonify(character), 200

@app.route('/characters', methods=['POST'])
def handle_add_character():
   body = request.get_json()

   new_character = Characters();
   new_character.name = body['name']
   new_character.type = body['type']
   new_character.age = body['age']
   new_character.heigth = body['heigth']
   new_character.affiliation = body['affiliation']
   
   db.session.add(new_character)
   db.session.commit()
   
   return jsonify(new_character.serialize()), 201

@app.route('/characters/<int:id>', methods=['DELETE'])
def handle_remove_character(id):
    character = Characters.query.get(id)
    db.session.delete(character)
    db.session.commit()

    return jsonify({}), 204


@app.route('/favorite/characters', methods=['POST'])
def add_people_favorite():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "Request body is missing"}), 400
    
    people_id = body.get('character_id')
    user_id = body.get('user_id')

    if not people_id or not user_id:
        return jsonify({"msg": "people_id and user_id are required"}), 400

    try:
        favorite = Fav_characters(people_id=people_id, user_id=user_id)
        db.session.add(favorite)
        people = Characters.query.get('character_id')
        people_serialize = people.serialize()
        
        if people_serialize["stars"] is None:
            people.stars = 1
        else:
            people.stars = people_serialize["stars"]+1

        db.session.commit()
        return jsonify(favorite.serialize()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    favorite = Fav_characters.query.filter_by(people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
