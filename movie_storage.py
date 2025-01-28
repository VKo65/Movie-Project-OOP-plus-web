import json
from colorama import Fore, Style



def get_movies():
    """
    Loads the movies from the JSON file and returns them as a dictionary.
    With try I will make sure, that there is the file data.json
    """

    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # no json. found
        print(Fore.RED + "The file 'data.json' was not found." + Style.RESET_ALL)
        return {}
    except json.JSONDecodeError:
        # json-file is empty or wrong structure
        print(
            Fore.RED + "The file 'data.json' is empty or wrong." + Style.RESET_ALL)
        return {}

def save_movies(movies):
    """get the movies data and save them to json data.json"""
    with open("data.json", "w") as file:
        json.dump(movies, file, indent=4)


def add_movie(title,year,rating):
    """
    adds the userinput from main to the json file.
    Return dictionary movies with added data for the function save_movies
    """
    movies = get_movies()

    if title in movies:
        print(f"Movie '{title}' already exists!")
        return
    movies[title] = {"year": year, "rating": rating}
    print(Fore.LIGHTYELLOW_EX + f"\nMovie '{title}' successfully added!\n" + Style.RESET_ALL)
    return movies


def delete_movie(title):
    """ delete the userinput from main from the json file.
    Return the reduced dictionary for the function save_movies
       """
    movies = get_movies()

    if title in movies:
        del movies[title]
    print(Fore.LIGHTGREEN_EX + "\nMovie deleted!" + Style.RESET_ALL)
    return movies

def update_movie(title, rating):
    """Update one single value of the json-file.
    Input of the variables title and rating, happens in main.py
    The new rating of the chosen movie, will be saved, after update."""
    movies = get_movies()
    if title in movies:
        year = movies[title]["year"]
        movies[title] = {"year": year, "rating": rating}
        with open("data.json", "w") as file:
            json.dump(movies, file, indent=4)
        print(Fore.LIGHTGREEN_EX + "Rating updated!" + Style.RESET_ALL)
