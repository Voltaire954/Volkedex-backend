# import requests
# import time
# from app import app, db
# from models import Pokemon

# LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=500"

# def get_all_pokemon_urls():
#     """Fetch ALL Pokémon URLs in one request."""
#     print("Fetching list of all Pokémon...")
#     data = requests.get(LIST_URL).json()
#     return [p["url"] for p in data["results"]]

# def fetch_pokemon_data(url):
#     """Fetch individual Pokémon data with retry logic."""
#     while True:
#         response = requests.get(url)

#         if response.status_code == 200:
#             return response.json()

#         print("Rate limiting... retrying in 1 sec...")
#         time.sleep(1)

# def seed_database():
#     with app.app_context():
#         print("Resetting database...")
#         db.drop_all()
#         db.create_all()

#         urls = get_all_pokemon_urls()

#         print(f"Found {len(urls)} Pokémon. Beginning download...\n")

#         for index, url in enumerate(urls, start=1):
#             print(f"[{index}/{len(urls)}] Fetching {url}")

#             data = fetch_pokemon_data(url)

#             # Extract types
#             types = [t["type"]["name"] for t in data["types"]]

#             pokemon = Pokemon(
#                 id=data["id"],
#                 name=data["name"],
#                 height=data["height"],
#                 weight=data["weight"],
#                 types=",".join(types)
#             )

#             db.session.add(pokemon)

#         db.session.commit()
#         print("\nDone! All Pokémon saved successfully.")

# if __name__ == "__main__":
#     seed_database()
# import requests
# import time
# from app import app, db
# from models import Pokemon  # MUST be imported before create_all()

# LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=500"#api call to pull 500 pokemon

# def get_all_pokemon_urls():#get all pokemon url
#     print("Fetching list of all Pokémon...")
#     data = requests.get(LIST_URL).json()#daata being inpuy on re
#     return [p["url"] for p in data["results"]]

# def fetch_pokemon_data(url):
#     while True:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()
#         print("Rate limiting... retrying in 1 sec...")
#         time.sleep(1)

# def seed_database():
#     with app.app_context():

#         print("Resetting database...")
#         db.drop_all()

#         # 👇 IMPORTANT: ensure Pokemon model is registered
#         from models import Pokemon

#         db.create_all()   # <-- Table is created here

#         urls = get_all_pokemon_urls()
#         print(f"Found {len(urls)} Pokémon. Beginning download...\n")

#         for index, url in enumerate(urls, start=1):
#             print(f"[{index}/{len(urls)}] Fetching {url}")

#             data = fetch_pokemon_data(url)
#             types = [t["type"]["name"] for t in data["types"]]

#             pokemon = Pokemon(
#                 id=data["id"],
#                 name=data["name"],
#                 height=data["height"],
#                 weight=data["weight"],
#                 types=",".join(types)
#             )

#             db.session.add(pokemon)

#         db.session.commit()
#         print("\nDone! All Pokémon saved successfully.")

# if __name__ == "__main__":
#     seed_database()
import requests                                   # For calling the PokeAPI
import time                                       # For sleep() when rate-limited
# Import your Flask app + database
from app import app, db
# Import Pokemon model so SQLAlchemy knows it
from models import Pokemon


LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=500"
# URL to get the first 500 Pokémon (names + URLs only)


def get_all_pokemon_urls():                       # Function to fetch all Pokémon URLs
    print("Fetching list of all Pokémon...")
    # Make request → convert JSON to Python
    data = requests.get(LIST_URL).json()
    # Return a list of Pokémon detail URLs
    return [p["url"] for p in data["results"]]


# Fetch a single Pokémon's full data
def fetch_pokemon_data(url):
    while True:                                   # Retry loop in case of rate limiting
        response = requests.get(url)

        if response.status_code == 200:           # If successful → return JSON
            return response.json()

        print("Rate limiting... retrying in 1 sec...")
        # Wait 1 second before retrying
        time.sleep(1)


def seed_database():                               # Main function to reset + seed the DB
    with app.app_context():                        # Ensures database functions have app context

        print("Resetting database...")
        db.drop_all()                              # Delete ALL tables in the database

        # Ensure model is registered before create_all()
        from models import Pokemon

        db.create_all()                            # Recreate tables fresh

        urls = get_all_pokemon_urls()              # Get list of 500 Pokémon URLs
        print(f"Found {len(urls)} Pokémon. Beginning download...\n")

        # Loop through every Pokémon URL
        for index, url in enumerate(urls, start=1):
            print(f"[{index}/{len(urls)}] Fetching {url}")

            # Pull full Pokémon JSON data
            data = fetch_pokemon_data(url)
            types = [t["type"]["name"] for t in data["types"]]
            # Extract list of Pokémon types

            pokemon = Pokemon(                     # Create Pokémon model instance
                id=data["id"],
                name=data["name"],
                height=data["height"],
                weight=data["weight"],
                # Join types → "grass, poison"
                types=",".join(types)
            )

            # Add Pokémon to current database session
            db.session.add(pokemon)

        db.session.commit()                        # Save ALL Pokémon to the database
        print("\nDone! All Pokémon saved successfully.")


if __name__ == "__main__":                         # Run only if script is executed directly
    seed_database()                                # Start seeding process
