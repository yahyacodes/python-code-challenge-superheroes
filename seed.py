from app import app, db, Hero, Power
from faker import Faker
import random

fake = Faker()

with app.app_context():
    # Seeding powers
    powers_data = [
        {"name": "Super Strength", "description": "Gives the wielder super-human strengths"},
        {"name": "Flight", "description": "Gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "Telekinesis", "description": "Allows the wielder to move objects with their mind"},
        {"name": "Invisibility", "description": "Makes the wielder invisible to the naked eye"},
    ]

    powers = [Power(**power) for power in powers_data]
    db.session.add_all(powers)
    db.session.commit()

    heroes_data = [
        {"name": "Clark Kent", "super_name": "Superman"},
        {"name": "Diana Prince", "super_name": "Wonder Woman"},
        {"name": "Bruce Wayne", "super_name": "Batman"},
        {"name": "Barry Allen", "super_name": "The Flash"},
    ]

    heroes = [Hero(**hero) for hero in heroes_data]
    db.session.add_all(heroes)
    db.session.commit()

    strengths = ["Strong", "Weak", "Average"]

    for hero in Hero.query.all():
        for _ in range(fake.random_int(1, 3)):
            power = random.choice(Power.query.all())
            hero_powers = hero.powers
            if power not in hero_powers:
                hero_powers.append(power)
                db.session.commit()

    print("🦸‍♂️ Done seeding!")