# POKEDEX KANTO-Version
# step 1 create a fetch that pulls from the api,
# step 2create a database using sqlite3-sequelize
# step 3 store data in a dattabase using sqlite3-sequelize
# step 4 test the databse and the information usint postman
# move on to react.js for frontend
# import requests

from flask import Flask, jsonify                # Import Flask (web server) + jsonify (return JSON)
from flask_sqlalchemy import SQLAlchemy          # Import SQLAlchemy for database work
from models import db, Pokemon                   # Bring in your db instance + Pokemon model
import requests                                  # For calling the external PokeAPI
from config import Config                        # App configuration (DB URL, settings)
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)                # Create the Flask app ONCE
app.config.from_object(Config)       # Load config
CORS(app)                            # Enable CORS

db.init_app(app)

@app.route("/")                                   # Route for the homepage
def home():                                       # Function handling requests to "/"
    return {"message": "Pokedex API is running!"} # Return simple message confirming API works


@app.route("/pokemon")                            # Route: GET all Pokémon
def get_allpokemon():                             # Function to fetch all Pokémon
    pokemons = Pokemon.query.all()                # Query all Pokémon from the database

    return jsonify([                               # Return result as JSON list
        {
            "id": p.id,                            # Pokémon ID
            "name": p.name,                        # Pokémon name
            "height": p.height,                    # Pokémon height
            "weight": p.weight,                    # Pokémon weight
            "types": p.types.split(",")            # Convert "fire, flying" → ["fire","flying"]
        }
        for p in pokemons                          # Loop over all Pokémon
    ])


@app.route("/pokemon/<name>")                      # Route: GET one Pokémon by name or ID
def get_pokemon(name):                             # Function takes dynamic path variable <name>

    if name.isdigit():                             # If input is all digits → treat it as an ID
        pokemon = Pokemon.query.filter_by(id=int(name)).first()
    else:                                           # Otherwise treat input as Pokémon name
        pokemon = Pokemon.query.filter_by(name=name.lower()).first()

    if not pokemon:                                 # If database did not return a Pokémon
        return jsonify({"error": "Pokemon not found in database"}), 404

    return jsonify({                                # Return Pokémon data as JSON
        "id": pokemon.id,
        "name": pokemon.name,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "types": pokemon.types.split(",")           # Convert types to list
    })


def fetch_and_store_pokemon(name):                 # Function to fetch Pokémon from PokeAPI & store locally
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"  # Build PokeAPI URL
    response = requests.get(url)                   # Call PokeAPI

    if response.status_code != 200:                # If Pokémon does not exist on PokeAPI
        return None                                # Return None to signal failure

    data = response.json()                         # Convert response JSON → Python dict

    types = ",".join([                             # Extract Pokémon types
        t['type']['name']                          # Each type name ("fire", "water", etc.)
        for t in data['types']                     # Loop through all type entries
    ])

    pokemon = Pokemon(                             # Create new Pokémon database object
        id=data["id"],                             # Pokémon ID
        name=data["name"],                         # Pokémon name
        height=data["height"],                     # Height from PokeAPI
        weight=data["weight"],                     # Weight from PokeAPI
        types=types                                # Store types as comma-separated string
    )

    db.session.add(pokemon)                        # Add Pokémon to session
    db.session.commit()                            # Save Pokémon to database

    return pokemon                                 # Return saved Pokémon object


if __name__ == "__main__":                         # Only run this block when file executed directly
    with app.app_context():                        # Needed to create DB tables
        db.create_all()
    port = int(os.environ.get("PORT", 5000))                           # Create tables only if they don’t already exist
    app.run(host="0.0.0.0", port=port)                           # Start Flask server in debug mode


# importpoke_url = "https://pokeapi.co/api/v2/"


# def get_pokemon_info(name):
#     url = f"{importpoke_url}/pokemon/{name}"
#     pokemon = requests.get(url).json()

#     # Collect ALL types into a list
#     types = []
#     for type_info in pokemon['types']:
#         types.append(type_info['type']['name'])

#     pokename = pokemon["name"]
#     id = pokemon["id"]
#     order = pokemon["order"]
#     height = pokemon["height"]
#     weight = pokemon["weight"]

#     print(f'name: {pokename}')
#     print(f'id: {id}')
#     print(f'order: {order}')
#     print(f'height: {height}')
#     print(f'weight: {weight}')
#     print("Types:", ", ".join(types))


# while True:
#     pokemon_name = input("search a pokemon: ")

#     get_pokemon_info(pokemon_name)

#     cont = input("would you like to search another? (Y/N): ").lower()
#     if cont == "n":
#         break
# from flask import Flask, jsonify            # Import Flask (web framework) and jsonify (convert data to JSON)
# from flask_sqlalchemy import SQLAlchemy      # Import SQLAlchemy database tools
# from models import db, Pokemon               # Import the database instance and Pokemon model
# import requests                              # Import requests to call external APIs (PokeAPI)
# from config import Config                    # Import your configuration settings


# app = Flask(__name__) #inbitiating flask app
# app.config.from_object(Config)#running configuration from config folder

# db.init_app(app)#initiating app into databse


# @app.route("/")#route for home page
# def home():#defining home function
#     return {"message": "Pokedex API is running!"}#print message to the terminal of ongoing api


# @app.route("/pokemon")#route method to get all pokemon
# def get_allpokemon():#defines a get all function that pulls all pokemon
#     pokemons = Pokemon.query.all()#query all pokemon into pokemons
#     """
#     returns a jsonify version of the pokemon data
#     """
#     return jsonify([{"id": p.id,
#                      "name": p.name,
#                      "height": p.height,
#                      "weight": p.weight,
#                      "types": p.types.split(",")}for p in pokemons])


# @app.route("/pokemon/<name>")#route for specific pokemon noame or id
# def get_pokemon(name):#defins get_pokemon function, passing in name to be searched for
#     if name.isdigit():#checks if what is passed is a digit, that way we can search using id.
#         pokemon = Pokemon.query.filter_by(id=int(name)).first()#filter the query of pokemon by id
#     else:
#         pokemon = Pokemon.query.filter_by(name=name.lower()).first()#filter the query of pokemon by name

#     if not pokemon:
#         return jsonify({"error": "Pokemon not found in database"}), 404#returns error if pokemon not in filtered search

#     return jsonify({
#         "id": pokemon.id,
#         "name": pokemon.name,
#         "height": pokemon.height,
#         "weight": pokemon.weight,
#         "types": pokemon.types.split(",")
#     })#returns the specific pokemon


# def fetch_and_store_pokemon(name):#fetch and store function
#     url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
#     response = requests.get(url)

#     if response.status_code != 200:
#         return None

#     data = response.json()
#     types = ",".join([t['type']['name'] for t in data['types']])

#     pokemon = Pokemon(
#         id=data["id"],
#         name=data["name"],
#         height=data["height"],
#         weight=data["weight"],
#         types=types
#     )
#     db.session.add(pokemon)
#     db.session.commit()

#     return pokemon


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
