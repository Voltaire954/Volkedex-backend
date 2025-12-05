from flask_sqlalchemy import SQLAlchemy          # Import SQLAlchemy ORM for database models


db = SQLAlchemy()                                # Create database instance (used by the app later)


class Pokemon(db.Model):                         # Define Pokémon table as a model
    __tablename__ = "pokemon"                    # Name of the table in the database

    id = db.Column(db.Integer, primary_key=True)
    # Primary key (unique ID for each Pokémon)

    name = db.Column(db.String, unique=True, nullable=False)
    # Pokémon name (must be unique, cannot be empty)

    height = db.Column(db.Integer, nullable=False)
    # Pokémon height from PokeAPI (stored as number)

    weight = db.Column(db.Integer, nullable=False)
    # Pokémon weight from PokeAPI (stored as number)

    types = db.Column(db.String, nullable=False)
    # Pokémon types stored as a single string, e.g. "grass, poison"
    # Later split into a list when returning JSON


# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Pokemon(db.Model):
#     __tablename__ = "pokemon"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)
#     height = db.Column(db.Integer, nullable=False)
#     weight = db.Column(db.Integer, nullable=False)
#     types = db.Column(db.String, nullable=False)  # "grass, poison"
