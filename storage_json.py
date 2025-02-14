import json
from istorage import IStorage


class StorageJson(IStorage):
    """
    A storage class that manages movies using a JSON file.
    Implements the IStorage interface.

    """
    def __init__(self, file_path):
        """Initializes the storage with a JSON file path."""
        self.file_path = file_path

    def _load_movies(self):
        """Loads movies from the JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            raise ValueError("The JSON file is corrupted.")

    def _save_movies(self, movies):
        """Saves movies to a JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """Returns all movies from the storage."""
        return self._load_movies()

    def add_movie(self, title, details):
        """Adds a new movie to the storage."""
        movies = self._load_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists.")
        movies[title] = details
        self._save_movies(movies)

    def delete_movie(self, title):
        """Deletes a movie from the storage."""
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        del movies[title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        """Updates the rating of a movie."""
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        movies[title]["rating"] = rating
        self._save_movies(movies)