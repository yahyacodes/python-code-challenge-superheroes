#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, hero_powers

from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'WELCOME TO SUPERHEROES APPLICATION'

## Routes

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()

    hero_list = [
        {'id': hero.id, 
         'name': hero.name, 
         'super_name': hero.super_name
         } 
         for hero in heroes]
    
    response = make_response(
        jsonify(hero_list), 200)
    
    return response

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return make_response(jsonify({'error': 'Hero not found'}), 404)

    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    response = make_response(
        jsonify(hero_data), 200)
    
    return response

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }

    response = make_response(
        jsonify(power_data), 200)
    
    return response

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({'error': 'Power not found'}), 404)

    data = request.get_json()
    if 'description' not in data:
        return make_response(
            jsonify({'error': 'Description is required'}), 400)

    description = data['description']
    power.description = description

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 500)

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }

    response = make_response(
        jsonify(power_data), 200)
    
    return response

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if not strength or not power_id or not hero_id:
        return make_response(jsonify({'errors': ['Validation errors']}), 400)

    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if not power or not hero:
        return make_response(jsonify({'error': 'Power or Hero not found'}), 404)

    hero_power = hero_powers(strength=strength, power=power, hero=hero)
    db.session.add(hero_power)
    db.session.commit()

    powers = [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }

    response = make_response(
        jsonify(hero_data), 200)
    
    return response


if __name__ == '__main__':
    app.run(port=5555)
