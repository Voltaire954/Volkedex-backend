import os    # Import OS module for handling file paths


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# BASE_DIR = the absolute path to the folder this file is in.
# Example: C:/Users/Chris/PokedexAPI/


DB_PATH = os.path.join(BASE_DIR, "pokedex.db")
# DB_PATH = BASE_DIR + "/pokedex.db"
# This creates a full path to your SQLite database file.


class Config:                                      # Configuration class for Flask settings
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    # Tells SQLAlchemy to use SQLite + the DB_PATH we created above.

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Turns off a feature that wastes memory.
